"""Worker threads for background processing."""
import threading
import queue
from pathlib import Path


class PipelineWorker:
    """Worker thread for running photogrammetry pipeline."""
    
    def __init__(self, pipeline, project_path, config, callback):
        """
        Initialize worker.
        
        Args:
            pipeline: PhotogrammetryPipeline instance
            project_path: Path to project directory
            config: Configuration dictionary
            callback: Callback function for progress updates
        """
        self.pipeline = pipeline
        self.project_path = project_path
        self.config = config
        self.callback = callback
        self.thread = None
        self.running = False
        self.output_queue = queue.Queue()
    
    def start(self):
        """Start the worker thread."""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
    
    def _run(self):
        """Run the pipeline in background thread."""
        try:
            def progress_callback(message):
                """Internal callback to queue messages."""
                self.output_queue.put(('progress', message))
                if self.callback:
                    self.callback(message)
            
            # Run the complete pipeline
            success, message, paths = self.pipeline.run_complete_pipeline(
                project_path=self.project_path,
                use_gpu=self.config.get('use_gpu', True),
                matcher_type=self.config.get('matcher_type', 'sequential'),
                include_dense=self.config.get('include_dense', False),
                callback=progress_callback
            )
            
            # Signal completion
            self.output_queue.put(('finished', (success, message, paths)))
            
        except Exception as e:
            self.output_queue.put(('error', str(e)))
        finally:
            self.running = False
    
    def is_running(self):
        """Check if worker is still running."""
        return self.running
    
    def get_message(self, timeout=0.1):
        """
        Get next message from queue.
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            Tuple of (message_type, message_data) or None
        """
        try:
            return self.output_queue.get(timeout=timeout)
        except queue.Empty:
            return None


class StepWorker:
    """Worker thread for running individual pipeline steps."""
    
    def __init__(self, step_func, callback):
        """
        Initialize step worker.
        
        Args:
            step_func: Function to execute
            callback: Callback for progress updates
        """
        self.step_func = step_func
        self.callback = callback
        self.thread = None
        self.running = False
        self.output_queue = queue.Queue()
    
    def start(self):
        """Start the worker thread."""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
    
    def _run(self):
        """Run the step in background thread."""
        try:
            def progress_callback(message):
                """Internal callback to queue messages."""
                self.output_queue.put(('progress', message))
                if self.callback:
                    self.callback(message)
            
            # Run the step function
            success, message = self.step_func(progress_callback)
            
            # Signal completion
            self.output_queue.put(('finished', (success, message)))
            
        except Exception as e:
            self.output_queue.put(('error', str(e)))
        finally:
            self.running = False
    
    def is_running(self):
        """Check if worker is still running."""
        return self.running
    
    def get_message(self, timeout=0.1):
        """
        Get next message from queue.
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            Tuple of (message_type, message_data) or None
        """
        try:
            return self.output_queue.get(timeout=timeout)
        except queue.Empty:
            return None


class DenseOnlyWorker:
    """Worker thread for running dense reconstruction on existing sparse model."""
    
    def __init__(self, pipeline, project_path, callback):
        """
        Initialize dense-only worker.
        
        Args:
            pipeline: PhotogrammetryPipeline instance
            project_path: Path to project directory with existing sparse model
            callback: Callback function for progress updates
        """
        self.pipeline = pipeline
        self.project_path = project_path
        self.callback = callback
        self.thread = None
        self.running = False
        self.output_queue = queue.Queue()
    
    def start(self):
        """Start the worker thread."""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
    
    def _run(self):
        """Run dense reconstruction in background thread."""
        try:
            def progress_callback(message):
                """Internal callback to queue messages."""
                self.output_queue.put(('progress', message))
                if self.callback:
                    self.callback(message)
            
            # Run dense reconstruction only
            success, message, paths = self.pipeline.run_dense_only(
                project_path=self.project_path,
                callback=progress_callback
            )
            
            # Signal completion
            self.output_queue.put(('finished', (success, message, paths)))
            
        except Exception as e:
            self.output_queue.put(('error', str(e)))
        finally:
            self.running = False
    
    def is_running(self):
        """Check if worker is still running."""
        return self.running
    
    def get_message(self, timeout=0.1):
        """
        Get next message from queue.
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            Tuple of (message_type, message_data) or None
        """
        try:
            return self.output_queue.get(timeout=timeout)
        except queue.Empty:
            return None


class DGUTWorker:
    """Worker thread for running 3D GRUT training."""
    
    def __init__(self, pipeline, project_path, config, callback):
        """
        Initialize 3D GRUT worker.
        
        Args:
            pipeline: PhotogrammetryPipeline instance
            project_path: Path to project directory with COLMAP sparse model
            config: Configuration dictionary with 3D GRUT settings
            callback: Callback function for progress updates
        """
        self.pipeline = pipeline
        self.project_path = project_path
        self.config = config
        self.callback = callback
        self.thread = None
        self.running = False
        self.output_queue = queue.Queue()
    
    def start(self):
        """Start the worker thread."""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
    
    def _run(self):
        """Run 3D GRUT training in background thread."""
        try:
            def progress_callback(message):
                """Internal callback to queue messages."""
                self.output_queue.put(('progress', message))
                if self.callback:
                    self.callback(message)
            
            # Get 3D GRUT configuration
            camera_model = self.config.get('camera_model', 'perspective')
            use_mcmc = self.config.get('dgut_mcmc', True)
            iterations = self.config.get('dgut_iterations', 30000)
            export_ply = self.config.get('dgut_export_ply', True)
            
            # Run 3D GRUT reconstruction
            success, message, output_path = self.pipeline.run_3dgut_reconstruction(
                project_path=self.project_path,
                camera_model=camera_model,
                use_mcmc=use_mcmc,
                iterations=iterations,
                export_ply=export_ply,
                callback=progress_callback
            )
            
            # Signal completion
            self.output_queue.put(('finished', (success, message, output_path)))
            
        except Exception as e:
            self.output_queue.put(('error', str(e)))
        finally:
            self.running = False
    
    def is_running(self):
        """Check if worker is still running."""
        return self.running
    
    def get_message(self, timeout=0.1):
        """
        Get next message from queue.
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            Tuple of (message_type, message_data) or None
        """
        try:
            return self.output_queue.get(timeout=timeout)
        except queue.Empty:
            return None


class DGUTWorker:
    """Worker thread for running 3D GRUT training."""
    
    def __init__(self, pipeline, project_path, config, callback):
        """
        Initialize 3D GRUT worker.
        
        Args:
            pipeline: PhotogrammetryPipeline instance
            project_path: Path to project directory with COLMAP sparse model
            config: Configuration dictionary with 3D GRUT settings
            callback: Callback function for progress updates
        """
        self.pipeline = pipeline
        self.project_path = project_path
        self.config = config
        self.callback = callback
        self.thread = None
        self.running = False
        self.output_queue = queue.Queue()
    
    def start(self):
        """Start the worker thread."""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
    
    def _run(self):
        """Run 3D GRUT training in background thread."""
        try:
            def progress_callback(message):
                """Internal callback to queue messages."""
                self.output_queue.put(('progress', message))
                if self.callback:
                    self.callback(message)
            
            # Get 3D GRUT configuration
            camera_model = self.config.get('camera_model', 'perspective')
            use_mcmc = self.config.get('dgut_mcmc', True)
            iterations = self.config.get('dgut_iterations', 30000)
            export_ply = self.config.get('dgut_export_ply', True)
            
            # Run 3D GRUT reconstruction
            success, message, output_path = self.pipeline.run_3dgut_reconstruction(
                project_path=self.project_path,
                camera_model=camera_model,
                use_mcmc=use_mcmc,
                iterations=iterations,
                export_ply=export_ply,
                callback=progress_callback
            )
            
            # Signal completion
            self.output_queue.put(('finished', (success, message, output_path)))
            
        except Exception as e:
            self.output_queue.put(('error', str(e)))
        finally:
            self.running = False
    
    def is_running(self):
        """Check if worker is still running."""
        return self.running
    
    def get_message(self, timeout=0.1):
        """
        Get next message from queue.
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            Tuple of (message_type, message_data) or None
        """
        try:
            return self.output_queue.get(timeout=timeout)
        except queue.Empty:
            return None
