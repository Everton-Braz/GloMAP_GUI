"""Pipeline orchestration for photogrammetry processing."""
import os
from pathlib import Path
from enum import Enum


class PipelineStep(Enum):
    """Enumeration of pipeline steps."""
    FEATURE_EXTRACTION = "Feature Extraction"
    FEATURE_MATCHING = "Feature Matching"
    SPARSE_RECONSTRUCTION = "Sparse Reconstruction (GloMAP)"
    EXPORT_SPARSE = "Export Sparse Point Cloud"
    IMAGE_UNDISTORTION = "Image Undistortion"
    STEREO_MATCHING = "Stereo Depth Computation"
    DENSE_FUSION = "Dense Point Cloud Fusion"
    DGUT_TRAINING = "3DGUT Training (Gaussian Splatting)"
    DGUT_EXPORT = "3DGUT Point Cloud Export"


class PhotogrammetryPipeline:
    """Manages the complete photogrammetry workflow."""
    
    def __init__(self, colmap_wrapper, glomap_wrapper, dgut_wrapper=None):
        """
        Initialize pipeline.
        
        Args:
            colmap_wrapper: COLMAPWrapper instance
            glomap_wrapper: GloMAPWrapper instance
            dgut_wrapper: DGUTWrapper instance (optional)
        """
        self.colmap = colmap_wrapper
        self.glomap = glomap_wrapper
        self.dgut = dgut_wrapper
        self.current_step = None
    
    def setup_workspace(self, project_path):
        """
        Create workspace directory structure.
        
        Args:
            project_path: Root path for the project
            
        Returns:
            Dictionary with paths for different components
        """
        project_path = Path(project_path)
        
        paths = {
            'project': project_path,
            'images': project_path / 'images',
            'database': project_path / 'database.db',
            'sparse': project_path / 'sparse',
            'sparse_0': project_path / 'sparse' / '0',
            'sparse_ply': project_path / 'sparse' / 'sparse.ply',
            'dense': project_path / 'dense',
            'dense_ply': project_path / 'dense' / 'fused.ply',
            'dgut': project_path / '3dgut',
            'dgut_ply': project_path / '3dgut' / 'pointcloud.ply'
        }
        
        # Create necessary directories
        for key in ['project', 'sparse', 'sparse_0', 'dense', 'dgut']:
            paths[key].mkdir(parents=True, exist_ok=True)
        
        return paths
    
    def run_feature_extraction(self, paths, use_gpu=True, max_features=8192, 
                              camera_model=None, camera_params=None, single_camera=False, callback=None):
        """
        Run feature extraction step.
        
        Args:
            paths: Dictionary of paths from setup_workspace
            use_gpu: Enable GPU acceleration
            max_features: Maximum features per image
            camera_model: Camera model for fisheye (e.g., 'OPENCV_FISHEYE')
            camera_params: Camera parameters string
            single_camera: Force single camera model
            callback: Progress callback function
            
        Returns:
            Tuple of (success, message)
        """
        self.current_step = PipelineStep.FEATURE_EXTRACTION
        
        if callback:
            callback(f"=== {PipelineStep.FEATURE_EXTRACTION.value} ===")
            if camera_model:
                callback(f"Using camera model: {camera_model}")
        
        return self.colmap.feature_extraction(
            database_path=paths['database'],
            image_path=paths['images'],
            use_gpu=use_gpu,
            max_features=max_features,
            camera_model=camera_model,
            camera_params=camera_params,
            single_camera=single_camera,
            callback=callback
        )
    
    def run_feature_matching(self, paths, matcher_type='sequential', overlap=10, callback=None):
        """
        Run feature matching step.
        
        Args:
            paths: Dictionary of paths from setup_workspace
            matcher_type: 'sequential' or 'exhaustive'
            overlap: Number of overlapping images (for sequential)
            callback: Progress callback function
            
        Returns:
            Tuple of (success, message)
        """
        self.current_step = PipelineStep.FEATURE_MATCHING
        
        if callback:
            callback(f"=== {PipelineStep.FEATURE_MATCHING.value} ===")
        
        if matcher_type == 'exhaustive':
            return self.colmap.exhaustive_matcher(
                database_path=paths['database'],
                callback=callback
            )
        else:
            return self.colmap.sequential_matcher(
                database_path=paths['database'],
                overlap=overlap,
                callback=callback
            )
    
    def run_sparse_reconstruction(self, paths, callback=None):
        """
        Run sparse reconstruction using GloMAP (if available) or COLMAP mapper.
        
        Args:
            paths: Dictionary of paths from setup_workspace
            callback: Progress callback function
            
        Returns:
            Tuple of (success, message)
        """
        self.current_step = PipelineStep.SPARSE_RECONSTRUCTION
        
        if callback:
            callback(f"=== {PipelineStep.SPARSE_RECONSTRUCTION.value} ===")
        
        # Try GloMAP first (10-100x faster)
        glomap_ok, _ = self.glomap.check_installation()
        
        if glomap_ok:
            if callback:
                callback("Using GloMAP for 10-100x faster reconstruction!")
            
            return self.glomap.mapper(
                database_path=paths['database'],
                image_path=paths['images'],
                output_path=paths['sparse'],
                callback=callback
            )
        else:
            # Fallback to COLMAP mapper
            if callback:
                callback("GloMAP not found - using COLMAP mapper (slower but reliable)")
            
            return self.colmap.mapper(
                database_path=paths['database'],
                image_path=paths['images'],
                output_path=paths['sparse_0'],
                callback=callback
            )
    
    def export_sparse_pointcloud(self, paths, callback=None):
        """
        Export sparse reconstruction to PLY format.
        
        Args:
            paths: Dictionary of paths from setup_workspace
            callback: Progress callback function
            
        Returns:
            Tuple of (success, message)
        """
        self.current_step = PipelineStep.EXPORT_SPARSE
        
        if callback:
            callback(f"=== {PipelineStep.EXPORT_SPARSE.value} ===")
        
        return self.colmap.model_converter(
            input_path=paths['sparse_0'],
            output_path=paths['sparse_ply'],
            output_type='PLY',
            callback=callback
        )
    
    def run_dense_reconstruction(self, paths, callback=None):
        """
        Run complete dense reconstruction pipeline.
        
        Args:
            paths: Dictionary of paths from setup_workspace
            callback: Progress callback function
            
        Returns:
            Tuple of (success, message)
        """
        # Step 1: Image Undistortion
        self.current_step = PipelineStep.IMAGE_UNDISTORTION
        if callback:
            callback(f"=== {PipelineStep.IMAGE_UNDISTORTION.value} ===")
        
        success, msg = self.colmap.image_undistorter(
            image_path=paths['images'],
            input_path=paths['sparse_0'],
            output_path=paths['dense'],
            callback=callback
        )
        
        if not success:
            return False, f"Image undistortion failed: {msg}"
        
        # Step 2: Stereo Depth Computation
        self.current_step = PipelineStep.STEREO_MATCHING
        if callback:
            callback(f"=== {PipelineStep.STEREO_MATCHING.value} ===")
        
        success, msg = self.colmap.patch_match_stereo(
            workspace_path=paths['dense'],
            callback=callback
        )
        
        if not success:
            return False, f"Stereo matching failed: {msg}"
        
        # Step 3: Depth Map Fusion
        self.current_step = PipelineStep.DENSE_FUSION
        if callback:
            callback(f"=== {PipelineStep.DENSE_FUSION.value} ===")
        
        success, msg = self.colmap.stereo_fusion(
            workspace_path=paths['dense'],
            output_path=paths['dense_ply'],
            callback=callback
        )
        
        return success, msg
    
    def run_dense_only(self, project_path, callback=None):
        """
        Run dense reconstruction on existing sparse model.
        
        Args:
            project_path: Root path for the project with existing sparse reconstruction
            callback: Progress callback function
            
        Returns:
            Tuple of (success, message, paths)
        """
        if callback:
            callback("========================================")
            callback("  Dense Reconstruction (Sparse Existing)")
            callback("========================================")
        
        # Setup workspace paths
        paths = self.setup_workspace(project_path)
        
        # Check if sparse reconstruction exists
        if not paths['sparse_0'].exists():
            return False, "No sparse reconstruction found. Run complete pipeline first.", paths
        
        # Check if images exist
        if not paths['images'].exists() or not any(paths['images'].iterdir()):
            return False, "No images found in images folder", paths
        
        # Run dense reconstruction
        success, msg = self.run_dense_reconstruction(paths, callback=callback)
        if not success:
            return False, f"Dense reconstruction failed: {msg}", paths
        
        if callback:
            callback("========================================")
            callback("  Dense Reconstruction Completed!")
            callback("========================================")
            callback(f"Dense point cloud: {paths['dense_ply']}")
        
        return True, "Dense reconstruction completed successfully", paths
    
    def run_3dgut_reconstruction(self, paths, camera_model='perspective', use_mcmc=True, 
                                iterations=30000, export_ply=True, callback=None):
        """
        Run 3DGUT Gaussian Splatting reconstruction.
        
        Args:
            paths: Dictionary of paths from setup_workspace
            camera_model: 'perspective' or 'fisheye'
            use_mcmc: Enable MCMC optimization
            iterations: Training iterations
            export_ply: Export point cloud after training
            callback: Progress callback function
            
        Returns:
            Tuple of (success, message)
        """
        if not self.dgut:
            return False, "3DGUT not initialized"
        
        # Check if 3DGUT is installed
        ok, msg = self.dgut.check_installation()
        if not ok:
            return False, f"3DGUT not available: {msg}"
        
        # Step 1: Train 3DGUT model
        self.current_step = PipelineStep.DGUT_TRAINING
        if callback:
            callback(f"=== {PipelineStep.DGUT_TRAINING.value} ===")
        
        success, msg = self.dgut.train(
            source_path=paths['images'],
            model_path=paths['dgut'],
            camera_model=camera_model,
            use_mcmc=use_mcmc,
            iterations=iterations,
            callback=callback
        )
        
        if not success:
            return False, f"3DGUT training failed: {msg}"
        
        # Step 2: Export to PLY (optional)
        if export_ply:
            self.current_step = PipelineStep.DGUT_EXPORT
            if callback:
                callback(f"=== {PipelineStep.DGUT_EXPORT.value} ===")
            
            success, msg = self.dgut.export_pointcloud(
                model_path=paths['dgut'],
                output_path=paths['dgut_ply'],
                num_points=1000000,
                callback=callback
            )
            
            if not success:
                if callback:
                    callback(f"Warning: Could not export point cloud: {msg}")
        
        return True, "3DGUT reconstruction completed successfully"
    
    def run_complete_pipeline(self, project_path, use_gpu=True, matcher_type='sequential',
                             include_dense=False, callback=None):
        """
        Run the complete photogrammetry pipeline.
        
        Args:
            project_path: Root path for the project
            use_gpu: Enable GPU acceleration
            matcher_type: 'sequential' or 'exhaustive'
            include_dense: Whether to run dense reconstruction
            callback: Progress callback function
            
        Returns:
            Tuple of (success, message, paths)
        """
        if callback:
            callback("========================================")
            callback("  GloMAP Photogrammetry Pipeline")
            callback("========================================")
        
        # Setup workspace
        paths = self.setup_workspace(project_path)
        
        # Check if images exist
        if not paths['images'].exists() or not any(paths['images'].iterdir()):
            return False, "No images found in images folder", paths
        
        # Feature Extraction
        success, msg = self.run_feature_extraction(paths, use_gpu=use_gpu, callback=callback)
        if not success:
            return False, f"Pipeline failed at feature extraction: {msg}", paths
        
        # Feature Matching
        success, msg = self.run_feature_matching(paths, matcher_type=matcher_type, callback=callback)
        if not success:
            return False, f"Pipeline failed at feature matching: {msg}", paths
        
        # Sparse Reconstruction (GloMAP)
        success, msg = self.run_sparse_reconstruction(paths, callback=callback)
        if not success:
            return False, f"Pipeline failed at sparse reconstruction: {msg}", paths
        
        # Export Sparse Point Cloud
        success, msg = self.export_sparse_pointcloud(paths, callback=callback)
        if not success:
            if callback:
                callback(f"Warning: Could not export sparse point cloud: {msg}")
        
        # Dense Reconstruction (optional)
        if include_dense:
            success, msg = self.run_dense_reconstruction(paths, callback=callback)
            if not success:
                return False, f"Pipeline failed at dense reconstruction: {msg}", paths
        
        if callback:
            callback("========================================")
            callback("  Pipeline Completed Successfully!")
            callback("========================================")
            callback(f"Sparse point cloud: {paths['sparse_ply']}")
            if include_dense:
                callback(f"Dense point cloud: {paths['dense_ply']}")
        
        return True, "Pipeline completed successfully", paths
