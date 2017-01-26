import numpy as np

def quantizer(mt,quant=3,A=1):
    bits = pow(2,quant)
    bitrange = (A-(-A))/(bits)

    bottom = -A
    lims=''
    binvals=''
    vals=''
    for i in range(0,bits):
        #bitlim_bottom = bitlim_bottom + (i*bitrange)
        #bitlim_top = bitlim_bottom + (-A+)
        if i is not (bits-1):
            lims=lims+'('+str(bottom+(i*bitrange))+'<=mt)&(mt<'+str(bottom+((i+1)*bitrange))+')'
        else:
            lims=lims+'('+str(bottom+(i*bitrange))+'<=mt)&(mt<='+str(bottom+((i+1)*bitrange))+')'
        lims=lims+','

        if i < bits/2:
            binvals=binvals+str(i)+','
        else:
            binvals=str(i)+','+binvals

        vals=vals+str(-A+((i+1)*bitrange))+','


    lims='['+lims[:-1]+']'
    binvals='['+binvals[:-1]+']'
    vals='['+vals[:-1]+']'
    #print(lims)
    #print(vals)
    pwmt=np.piecewise(mt,eval(lims),eval(binvals))
    return(pwmt)
