import math

class Utils:
    """
    Utility class storing various helper methods used across the application
    """
    
    def lerp(A, B, t):
        """
        Linear interpolation using a linear function from point A to point B which returns a point on the x axis between those points at 
        percentage t of the line

        Args:
            A (int): The start x coordinate of the line
            B (int): The end x coordinate of the line
            t (int): Percentage to update the start x coordinate up to the end x coordinate (value between 0 and 1)

        Returns:
            int: The x value between A and B on the line at "t" percent
        """

        return A+(B-A)*t
    
    def get_intersection(A, B, C ,D):
        """
        Helper method checking if there is an intersection between two segments A-B and C-D
        using linear interpolation on both segments and seeing if they are equal on a given t

        We basically write down both lerp functions for x and y for both segments and equalize them. Then we solve the equation for 
        t and since the two lerp equations were equalized, t is where our intersection is. Now we only need to use that t as the percent in our lerp 
        functions to obtain the x and y values of our point.

        Args:
            A (dict): The start point of the first segment
            B (dict): The end point of the first segment
            C (dict): The start point of the second segment
            D (dict): The end point of the second segment

        Returns: 
            dict: The point of the intersection and its offset/the percent in the lerp function
            none: If there was no intersection

        """

        t_Top = (D["x"]-C["x"])*(A["y"]-C["y"])-(D["y"]-C["y"])*(A["x"]-C["x"]) # Numerator of the equation to obtain t
        u_Top = (C["y"]-A["y"])*(A["x"]-B["x"])-(C["x"]-A["x"])*(A["y"]-B["y"]) # Numerator of the equation to obtain u
        bottom = (D["y"]-C["y"])*(B["x"]-A["x"])-(D["x"]-C["x"])*(B["y"]-A["y"]) # Denominator of the to obtain t;u

        if(bottom !=0 ): # Make sure that the denominator of the division is not 0
            t = t_Top/bottom
            u = u_Top/bottom
            if(t >= 0 and t <= 1 and u >= 0 and u <= 1):
                return{
                    "x":Utils.lerp(A["x"],B["x"],t),
                    "y":Utils.lerp(A["y"],B["y"],t),
                    "offset" : t}
                
        return None
    
    def polys_intersect(poly1, poly2):
        """
        Checks if there is an intersection between two polygons

        Args:
            poly1 (list): The first polygon 
            poly2 (list): The second polygon 

        Returns:
            bool: True if there is an intersection, else false
        """

        for i in range(len(poly1)):
            for j in range(len(poly2)):
                touch = Utils.get_intersection(
                    poly1[i],
                    poly1[(i+1)%len(poly1)],
                    poly2[j],
                    poly2[(j+1)%len(poly2)]
                )
                if touch:
                    return True
                
        return False
