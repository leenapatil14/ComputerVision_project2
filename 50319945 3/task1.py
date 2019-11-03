"""
RANSAC Algorithm Problem
(Due date: Oct. 23, 3 P.M., 2019)
The goal of this task is to fit a line to the given points using RANSAC algorithm, and output
the names of inlier points and outlier points for the line.

Do NOT modify the code provided to you.
Do NOT use ANY API provided by opencv (cv2) and numpy (np) in your code.
Do NOT import ANY library (function, module, etc.).
You can use the library random
Hint: It is recommended to record the two initial points each time, such that you will Not 
start from this two points in next iteration.
"""
import random
def solution(input_points, t, d, k):
    """
    :param input_points:
           t: t is the perpendicular distance threshold from a point to a line
           d: d is the number of nearby points required to assert a model fits well, you may not need this parameter
           k: k is the number of iteration times
           Note that, n for line should be 2
           (more information can be found on the page 90 of slides "Image Features and Matching")
    :return: inlier_points_name, outlier_points_name
    inlier_points_name and outlier_points_name is two list, each element of them is str type.
    For example: If 'a','b' is inlier_points and 'c' is outlier_point.
    the output should be two lists of ['a', 'b'], ['c'].
    Note that, these two lists should be non-empty.
    """
    # TODO: implement this function.
    #list to store visited samples
    prev=[]
    final_inliers=[]
    final_outliers=[]
    max_point=[]
    sum_distance=0
    min_error=99999
    #repeat for 'k' iterations
    for i in range(k):
        
        #get ramdom samples of two points
        points=random.sample(input_points,2)
        #print(points)
        point=[points[0]['name'],points[1]['name']]
        #print("POINT",point[::-1],point)
        #check if point is not already visited
        if (point not in prev) and (point[::-1] not in prev):
            inliers=[]
            outliers=[]
            prev.append([points[0]['name'],points[1]['name']])
            
            #print("\n",prev)
            #get line from sample points
            m=1
            y_diff=points[0]['value'][1]-points[1]['value'][1]
            x_diff=points[0]['value'][0]-points[1]['value'][0]
            if(x_diff!=0):
                m=y_diff/x_diff
                A_perp=m
                B_perp=-1
                c=points[0]['value'][1]-(m*points[0]['value'][0])
           #handle parametersfor for the y-axis
            else:
                A_perp=m
                B_perp=0
                c=0
            #print("C",c,m,points[0]['value'][0])
            C_perp=c
            
            sum_distance=0
            #calcuate the distance of saple point from all other points other than the sample points
            for dict_p in input_points:
                if dict_p['name'] not in point:
                    x=dict_p['value'][0]
                    y=dict_p['value'][1]
                    distance=abs((A_perp*x)+(B_perp*y)+C_perp)/((A_perp*A_perp)+(B_perp*B_perp))**0.5
                    #print(distance)
                    #if distance less than threshold, count inliers and outliers, also find total distance of all inliers
                    if distance<t:
                        inliers.append(dict_p['name'])
                        sum_distance+=distance
                    else:
                        outliers.append(dict_p['name'])
            avg=0
            #check number of inliers
            if len(inliers)>=d:
                #find avg of inlier's distances
                avg=sum_distance/len(inliers)
                #store point with minimum avgs(error)
                if avg<min_error:
                    min_error=avg
                    max_point=point
                    final_inliers=inliers
                    final_outliers=outliers
                #print("current_point",point)
                
                #print("\n",(inliers),"\n",(outliers),avg,sum_distance)
    #print("\n","\n","Max",max_point)
    final_inliers.append(max_point[0])
    final_inliers.append(max_point[1])
    #print("\n",(final_inliers),"\n",(final_outliers))
            
    return final_inliers,final_outliers
    #raise NotImplementedError


if __name__ == "__main__":
    input_points = [{'name': 'a', 'value': (0.0, 1.0)}, {'name': 'b', 'value': (2.0, 1.0)},
                    {'name': 'c', 'value': (3.0, 1.0)}, {'name': 'd', 'value': (0.0, 3.0)},
                    {'name': 'e', 'value': (1.0, 2.0)}, {'name': 'f', 'value': (1.5, 1.5)},
                    {'name': 'g', 'value': (1.0, 1.0)}, {'name': 'h', 'value': (1.5, 2.0)}]
    t = 0.5
    d = 3
    k = 100
    inlier_points_name, outlier_points_name = solution(input_points, t, d, k)  # TODO
    assert len(inlier_points_name) + len(outlier_points_name) == 8  
    f = open('./results/task1_result.txt', 'w')
    f.write('inlier points: ')
    for inliers in inlier_points_name:
        f.write(inliers + ',')
    f.write('\n')
    f.write('outlier points: ')
    for outliers in outlier_points_name:
        f.write(outliers + ',')
    f.close()


