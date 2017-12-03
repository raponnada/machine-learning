from math import sqrt, acos, pi
from decimal import Decimal, getcontext

getcontext().prec = 30


class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG = 'Only defined in two three dimensions'

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(self.coordinates)
            # print self.coordinates
            # print self.dimension

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def magnitude(self):
        coordinates_squared = [x**2 for x in self.coordinates]
        return Decimal(sqrt(sum(coordinates_squared)))

    def normalized(self):
        try:
            magnitude = self.magnitude()
            return self.times_scalar(Decimal(1.0) / magnitude)
        except ZeroDivisionError:
            raise Exception('Cannot normalize the zero vector')

    def plus(self, v):
        new_coordinates = [x + y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def minus(self, v):
        new_coordinates = [x - y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scalar(self, magnitude):
        new_coordinates = [magnitude * x for x in self.coordinates]
        return Vector(new_coordinates)

    def dot_product(self, v):
        new_coordinates = [x * y for x, y in zip(self.coordinates, v.coordinates)]
        return sum(new_coordinates)

    def angle(self, v, in_degrees=False):
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            dot = u1.dot_product(u2)
            angle_in_radius = acos(round(dot, 10))

            if in_degrees:
                degrees_per_radian = 180. / pi
                return angle_in_radius * degrees_per_radian
            else:
                return angle_in_radius
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with the zero vector')
            else:
                raise e

    def is_orthogonal_to(self, v, tolerance=1e-10):
        return abs(self.dot_product(v)) < tolerance

    def is_parallel_to(self, v):
        return (self.is_zero() or v.is_zero() or self.angle(v) == 0 or self.angle(v) == pi)

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def component_parallel_to(self, v):
        try:
            ub = v.normalized()
            dot_product = self.dot_product(ub)
            return ub.times_scalar(dot_product)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with the zero vector')
            else:
                raise e

    def component_orthogonal_to(self, v):
        try:
            projection = self.component_parallel_to(v)
            return self.minus(projection)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with the zero vector')
            else:
                raise e

    def area_of_triangle(self, v):
        return self.area_of_parallelogram(v) / Decimal('2.0')

    def area_of_parallelogram(self, v):
        cross_product = self.cross_product(v)
        return cross_product.magnitude()

    def cross_product(self, v):
        try:
            x_1, y_1, z_1 = self.coordinates
            x_2, y_2, z_2 = v.coordinates
            new_coordinates = [y_1 * z_2 - y_2 * z_1, -
                               (x_1 * z_2 - x_2 * z_1), x_1 * y_2 - x_2 * y_1]
            return Vector(new_coordinates)
        except ValueError as e:
            msg = str(e)
            if msg == 'need more than 2 values to unpack':
                self_embedded_in_R3 = Vector(self.coordinates + ('0',))
                v_embedded_in_R3 = Vector(v.coordinates + ('0',))
                return self_embedded_in_R3.cross_product(v_embedded_in_R3)
            elif(msg == 'too many values to unpack' or msg == 'need more than 1 value to unpack'):
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
            else:
                raise e


# v = Vector([-0.221, 7.437])
# print v.magnitude()
# v = Vector([8.813, -1.331, -6.247])
# print v.magnitude()
# v = Vector([5.581, -2.136])
# print v.normalized()
# v = Vector([1.996, 3.108, -4.554])
# print v.normalized()

# v = Vector([7.887, 4.138])
# w = Vector([-8.802, 6.776])
# print v.dot_product(w)
# v = Vector([3.183, -7.627])
# w = Vector([-2.668, 5.319])
# print v.angle(w)
# v = Vector([-5.955, -4.904, -1.874])
# w = Vector([-4.496, -8.755, 7.103])
# print v.dot_product(w)
# v = Vector([7.35, 0.221, 5.188])
# w = Vector([2.751, 8.259, 3.985])
# print v.angle(w, in_degrees=True)

# v = Vector(['-7.579', '-7.88'])
# w = Vector(['22.737', '23.64'])
# print 'is parallel:', v.is_parallel_to(w)
# print 'is orthogonal', v.is_orthogonal_to(w)
#
# v = Vector(['-2.029', '9.97', '4.172'])
# w = Vector(['-9.231', '-6.639', '-7.245'])
# print 'is parallel:', v.is_parallel_to(w)
# print 'is orthogonal', v.is_orthogonal_to(w)
#
# v = Vector(['-2.328', '-7.284', '-1.214'])
# w = Vector(['-1.821', '1.072', '-2.94'])
# print 'is parallel:', v.is_parallel_to(w)
# print 'is orthogonal', v.is_orthogonal_to(w)
#
# v = Vector(['2.118', '4.827'])
# w = Vector(['0', '0'])
# print 'is parallel:', v.is_parallel_to(w)
# print 'is orthogonal', v.is_orthogonal_to(w)

# v = Vector(['3.039', '1.879'])
# b = Vector(['0.825', '2.036'])
# print v.component_parallel_to(b)
# v = Vector(['-9.88', '-3.264', '-8.159'])
# b = Vector(['-2.155', '-9.353', '-9.473'])
# print v.component_orthogonal_to(b)
# v = Vector(['3.009', '-6.172', '3.692', '-2.51'])
# b = Vector(['6.404', '-9.144', '2.759', '8.718'])
# print v.component_parallel_to(b)
# print v.component_orthogonal_to(b)


# v = Vector(['8.462', '7.893', '-8.187'])
# w = Vector(['6.984', '-5.975', '4.778'])
# print v.cross_product(w)
# v = Vector(['-8.987', '-9.838', '5.031'])
# w = Vector(['-4.268', '-1.861', '-8.866'])
# print v.area_of_parallelogram(w)
# v = Vector(['1.5', '9.547', '3.691'])
# w = Vector(['-6.007', '0.124', '5.772'])
# print v.area_of_triangle(w)
