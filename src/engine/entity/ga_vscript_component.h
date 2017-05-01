#ifndef GA_VSCRIPT_COMPONENT_H
#define GA_VSCRIPT_COMPONENT_H

#include "ga_component.h"
#include "vscript.h"

class ga_vscript_component : public ga_component
{
public:
	ga_vscript_component(class ga_entity* ent, void (*func)(void*, void*));
	virtual ~ga_vscript_component();

	virtual void update(struct ga_frame_params* params) override;
	
protected:
	void (*_func)(void*, void*);
};

#endif //GA_VSCRIPT_COMPONENT_H