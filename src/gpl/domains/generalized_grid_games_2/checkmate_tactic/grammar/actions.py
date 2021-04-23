def encode_op(piece, o):
    return "{}_{}.{}_{}.{}".format(piece, o[0][0], o[0][1], o[1][0], o[1][1])