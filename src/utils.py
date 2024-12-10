import pymunk

def create_segment(pos1, pos2, width, space):
    segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    segment_shape = pymunk.Segment(segment_body, pos1, pos2, width)
    segment_shape.elasticity = 1
    segment_body.friction = 0.5
    space.add(segment_body, segment_shape)