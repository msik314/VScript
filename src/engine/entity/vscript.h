#ifdef VSCRIPT
#undef VSCRIPT

#include "ga_component.h"
#include "ga_entity.h"
#include "framework/ga_frame_params.h"
#include "math/ga_vec3f.h"

typedef void* Reference;

Reference ga_vscript_get_entity(Reference component)
{
	return ((ga_component*)component)->get_entity();
}

bool ga_vscript_get_input_left(Reference params)
{
	ga_frame_params* frame_params = (ga_frame_params*)params;
	return frame_params->_button_mask & k_button_g;
}

bool ga_vscript_get_input_right(Reference params)
{
	ga_frame_params* frame_params = (ga_frame_params*)params;
	return frame_params->_button_mask & k_button_h;
}

bool ga_vscript_translate(Reference entity, float x, float y, float z)
{
	ga_entity* e = (ga_entity*)entity;
	ga_vec3f translation;
	translation.x = x;
	translation.y = y;
	translation.z = z;
	e->translate(translation);
}
#endif //VSCRPT_H