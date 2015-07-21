import sys

def create_mask(maskl, maskr):
    if (maskl <= maskr):
        return ((1 << (maskr - maskl + 1)) - 1) << (31 - maskr)
    else:
        return (~create_mask(maskr+1, maskl-1)) & 0xFFFFFFFF

def rotate_left(val, r_bits, max_bits=32):
    (val << r_bits%max_bits) & (2**max_bits-1) | \
            ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))

def rotate_right(val, r_bits, max_bits=32):
    return ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
                (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

def get_mask(rot,maskl,maskr):
    return rotate_right(create_mask(maskl,maskr), rot)

def get_shift_type(rot,maskl,maskr):
    """ FIXME """
    if rot == 0:
        return "<<"
    elif maskr+rot > 31:
        return ">>"
    else:
        return "<<"

def get_shift_amt(rot,maskl,maskr):
    """ FIXME """
    if rot == 0:
        return 0
    elif maskr+rot <= 31:
        return rot
    else:
        return 32 - rot

'''
rot = 28
maskl = 0
maskr = 7
'''

def show_usage(argv):
    print "Usage: python %s <rot> <maskl> <maskr>" % (argv[0])
    print "\tex: rlwinm r3, r4, 8, 24, 27"
    print "\tinput: python %s 8 24 27" % (argv[0])

def main():
    if len(sys.argv) != 4:
        show_usage(sys.argv)
        return
    rot   = int(sys.argv[1])
    maskl = int(sys.argv[2])
    maskr = int(sys.argv[3])
    assert maskl <= maskr
    assert 32 - (rot + maskr-maskl) > 0
    print "rlwinm rX, rY, %d, %d, %d" % (rot,maskl,maskr)
    print "rX = (rY & 0x%08x) %s %d;" % (get_mask(rot,maskl,maskr), get_shift_type(rot,maskl,maskr), get_shift_amt(rot,maskl,maskr))
    return

if __name__ == "__main__":
    main()

