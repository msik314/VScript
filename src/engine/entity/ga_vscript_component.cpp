#include "ga_vscript_component.h"

#include "entity/ga_entity.h"
#include "framework/ga_frame_params.h"

ga_vscript_component::ga_vscript_component(ga_entity* ent, void (*func)(void*, void*)):
	ga_component(ent)
{
	_func = func;
}

ga_vscript_component::~ga_vscript_component(){}

void ga_vscript_component::update(ga_frame_params* params)
{
	_func(this, params);
}