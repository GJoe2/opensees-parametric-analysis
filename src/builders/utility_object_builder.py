"""
Utility object builder for model utilities and encoding functions.
"""

class UtilityBuilder:
    """
    Utility builder for general model-related functions.
    Encapsulates encoding and dimension calculations for models.
    """
    @staticmethod
    def generate_model_name(L_B_ratio: float, B: float, nx: int, ny: int) -> str:
        """
        Generate encoded name for the model.
        Args:
            L_B_ratio: L/B ratio (aspect ratio)
            B: Width of the structure in meters
            nx: Number of axes in X direction
            ny: Number of axes in Y direction
        Returns:
            Encoded model name (e.g., F01_15_10_1224)
        """
        aspect_code = int(L_B_ratio * 10)
        B_code = int(B)
        grid_code = nx * 100 + ny
        return f"F01_{aspect_code:02d}_{B_code:02d}_{grid_code:04d}"

    @staticmethod
    def calculate_dimensions(L_B_ratio: float, B: float) -> tuple:
        """
        Calculate L and B dimensions based on L/B ratio.
        Args:
            L_B_ratio: L/B ratio
            B: Width of the structure in meters
        Returns:
            Tuple with (L, B) in meters
        """
        L = B * L_B_ratio
        return L, B

    @staticmethod
    def create(L_B_ratio: float, B: float, nx: int, ny: int) -> dict:
        """
        Create a general object summary for model encoding and dimensions.
        Args:
            L_B_ratio: L/B ratio
            B: Width of the structure in meters
            nx: Number of axes in X direction
            ny: Number of axes in Y direction
        Returns:
            Dictionary with model_name and dimensions
        """
        model_name = UtilityBuilder.generate_model_name(L_B_ratio, B, nx, ny)
        L, B = UtilityBuilder.calculate_dimensions(L_B_ratio, B)
        return {
            'model_name': model_name,
            'dimensions': {'L': L, 'B': B}
        }
