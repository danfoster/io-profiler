#!/usr/sbin/dtrace -s

#pragma D option quiet

io:::start { 
    this->size = args[0]->b_bcount;
    this->dev = (string)args[1]->dev_name;

    /* store details */
    @Size[this->dev] = quantize(this->size);
} 

tick-10s
{
    printa(@Size);
    exit(0)
}