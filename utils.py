import math

class Utils:
    
    def lerp(A, B, t):
        return A+(B-A)*t
    
    def get_intersection(A, B, C ,D):
        t_Top = (D["x"]-C["x"])*(A["y"]-C["y"])-(D["y"]-C["y"])*(A["x"]-C["x"])
        u_Top = (C["y"]-A["y"])*(A["x"]-B["x"])-(C["x"]-A["x"])*(A["y"]-B["y"])
        bottom = (D["y"]-C["y"])*(B["x"]-A["x"])-(D["x"]-C["x"])*(B["y"]-A["y"])

        if(bottom !=0 ):
            t = t_Top/bottom
            u = u_Top/bottom
            if(t >= 0 and t <= 1 and u >= 0 and u <= 1):
                return{
                    "x":Utils.lerp(A["x"],B["x"],t),
                    "y":Utils.lerp(A["y"],B["y"],t),
                    "offset" : t}
                
        return None
    
    def polys_intersect(poly1, poly2):
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
