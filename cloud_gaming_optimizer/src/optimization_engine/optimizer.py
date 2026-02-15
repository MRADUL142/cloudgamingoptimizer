"""Gaming Optimizer - Main optimization orchestrator."""

import logging
from typing import Dict, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class GamingOptimizer:
    """Main orchestrator for cloud gaming optimization."""
    
    def __init__(self, optimization_rules: Any = None, ml_model: Optional[Any] = None):
        """
        Initialize gaming optimizer.
        
        Args:
            optimization_rules: OptimizationRules instance
            ml_model: Trained ML model for predictions (optional)
        """
        self.optimization_rules = optimization_rules
        self.ml_model = ml_model
        self.optimization_history = []
    
    def optimize(self, network_metrics: Dict, system_metrics: Dict, 
                game_info: Optional[Dict] = None, quality_preference: str = "balanced") -> Dict[str, Any]:
        """
        Run full optimization pipeline.
        
        Args:
            network_metrics: Network metrics dictionary
            system_metrics: System metrics dictionary
            game_info: Information about the game (optional)
            quality_preference: User quality preference
            
        Returns:
            Optimization result dictionary
        """
        timestamp = datetime.now().isoformat()
        
        # Get rules-based recommendations
        if self.optimization_rules:
            settings = self.optimization_rules.generate_recommendations(
                network_metrics, system_metrics, quality_preference
            )
            explanations = self.optimization_rules.get_optimization_explanation(
                settings, network_metrics, system_metrics
            )
        else:
            settings = None
            explanations = {}
        
        # ML predictions (if model available)
        ml_predictions = {}
        if self.ml_model:
            try:
                ml_predictions = self._get_ml_predictions(network_metrics, system_metrics, game_info)
            except Exception as e:
                logger.warning(f"ML prediction failed: {e}")
        
        # Combine results
        result = {
            "timestamp": timestamp,
            "network_metrics": network_metrics,
            "system_metrics": system_metrics,
            "recommendations": {
                "resolution": settings.resolution if settings else "1080p",
                "fps": settings.fps if settings else 60,
                "bitrate_mbps": settings.bitrate if settings else 25,
                "server_region": settings.server_region if settings else "default",
                "priority": settings.priority if settings else "balanced"
            },
            "explanations": explanations,
            "ml_predictions": ml_predictions,
            "applied": False
        }
        
        self.optimization_history.append(result)
        
        logger.info(f"Optimization complete - Resolution: {result['recommendations']['resolution']}, "
                   f"FPS: {result['recommendations']['fps']}, Bitrate: {result['recommendations']['bitrate_mbps']}Mbps")
        
        return result
    
    def _get_ml_predictions(self, network_metrics: Dict, system_metrics: Dict, 
                           game_info: Optional[Dict] = None) -> Dict[str, float]:
        """
        Get predictions from ML model.
        
        Args:
            network_metrics: Network metrics
            system_metrics: System metrics
            game_info: Game information
            
        Returns:
            ML predictions dictionary
        """
        # Prepare features for ML model
        features = self._prepare_ml_features(network_metrics, system_metrics, game_info)
        
        # Get predictions
        predictions = {}
        
        try:
            # Example: predict latency impact on smoothness (0-1 scale)
            smoothness_score = self.ml_model.predict([features])[0]
            predictions['smoothness_score'] = min(1.0, max(0.0, smoothness_score))
        except Exception as e:
            logger.warning(f"Smoothness prediction failed: {e}")
        
        return predictions
    
    def _prepare_ml_features(self, network_metrics: Dict, system_metrics: Dict, 
                            game_info: Optional[Dict] = None) -> list:
        """
        Prepare features for ML model.
        
        Args:
            network_metrics: Network metrics
            system_metrics: System metrics
            game_info: Game information
            
        Returns:
            Feature list for ML model
        """
        features = [
            network_metrics.get('ping_ms', 0),
            network_metrics.get('jitter_ms', 0),
            network_metrics.get('packet_loss_percent', 0),
            system_metrics.get('cpu_percent', 0),
            system_metrics.get('ram_percent', 0),
            system_metrics.get('gpu_percent', 0),
            0  # placeholder for additional features
        ]
        
        return features
    
    def apply_optimization(self, result: Dict, apply_func: Any = None) -> bool:
        """
        Apply optimization settings to system.
        
        Args:
            result: Optimization result
            apply_func: Function to apply settings (optional)
            
        Returns:
            True if applied successfully
        """
        try:
            if apply_func:
                apply_func(result['recommendations'])
            
            # Mark as applied
            result['applied'] = True
            result['applied_timestamp'] = datetime.now().isoformat()
            
            logger.info("Optimization applied successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to apply optimization: {e}")
            return False
    
    def get_history(self, limit: int = 100) -> list:
        """
        Get optimization history.
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List of optimization results
        """
        return self.optimization_history[-limit:]
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics from optimization history.
        
        Returns:
            Statistics dictionary
        """
        if not self.optimization_history:
            return {"error": "No optimization history"}
        
        import statistics
        
        fps_values = [r['recommendations']['fps'] for r in self.optimization_history]
        bitrate_values = [r['recommendations']['bitrate_mbps'] for r in self.optimization_history]
        
        return {
            "total_optimizations": len(self.optimization_history),
            "avg_fps": round(statistics.mean(fps_values), 1),
            "avg_bitrate_mbps": round(statistics.mean(bitrate_values), 1),
            "most_common_resolution": max(
                set([r['recommendations']['resolution'] for r in self.optimization_history]),
                key=[r['recommendations']['resolution'] for r in self.optimization_history].count
            )
        }
    
    def reset_history(self):
        """Clear optimization history."""
        self.optimization_history = []
        logger.info("Optimization history cleared")
