#!/usr/sbin/dtrace -s

#pragma D option quiet

io:::start 
/args[0]->b_flags & B_READ/
{
    this->size = args[0]->b_bcount;
    this->dev = (string)args[1]->dev_pathname;

    /* store details */
    @Size[this->dev,"read"] = quantize(this->size);
} 

io:::start 
/args[0]->b_flags & B_WRITE/
{
    this->size = args[0]->b_bcount;
    this->dev = (string)args[1]->dev_pathname;

    /* store details */
    @Size[this->dev,"write"] = quantize(this->size);
} 

tick-300s
{
    printa(@Size);
    exit(0)
}
