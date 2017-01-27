import numpy as np

def quantizer(mt,quant,A=1):
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

def unquantizer(pwmt,quant):
    pwmt=np.asarray(pwmt)
    bits=pow(2,quant)
    lims=''
    for i in range(0,bits):
        lims=lims+'(pwmt=='+str(i)+')'
        lims=lims+','
    lims='['+lims[:-1]+']'
    vals=np.arange(0,bits/2).tolist()+(np.arange(-1,-1-bits/2,-1).tolist())
    mt=np.piecewise(pwmt,eval(lims),vals)
    return(mt)
