from spider import *
from spider import _ok
content.grid(column=0, row=0,sticky=(N, S, E, W))
Labelurl.grid(column=0, row=0,columnspan=4, rowspan=1,pady=5,padx=3)

lf.grid(column=0, row=1,columnspan=4,sticky=(N, S, E, W), rowspan=1,pady=10,padx=3)

namelbl.grid(column=0, row=0)
name.grid(column=1, row=0,columnspan=2,rowspan=1)
example.grid(column=3, row=0)


ok.grid(column=0, row=3)
output.grid(column=1, row=3)
Set.grid(column=2, row=3)
Exit.grid(column=3, row=3)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=1)
content.columnconfigure(1, weight=1)
content.columnconfigure(2, weight=1)
content.columnconfigure(3, weight=1)
content.rowconfigure(1, weight=1)

root.bind('<Return>',_ok)

root.mainloop()
