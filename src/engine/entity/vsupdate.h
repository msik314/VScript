#include "vscript.h"

void vsupdate(Reference component, Reference params)
{
bool right;
bool left;
Reference entity;
entity = ga_vscript_get_entity(component);
left = ga_vscript_get_input_left(params);

right = ga_vscript_get_input_right(params);
if(left)
goto Block1;
else
goto Block2;
Block1:
ga_vscript_translate(entity, -1, 0, 0);
goto Block2;
Block2:
if(right)
goto Block3;
else
goto Block4;
Block3:
ga_vscript_translate(entity, 1, 0, 0);
goto Block4;
Block4:
return ;
}
