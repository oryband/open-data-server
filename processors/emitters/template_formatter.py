import pystache

from base import Emitter
from internal_db_ops import internal_find

@Emitter.emitter
class TemplateFormatter(Emitter):
    
    def condition(self):
        format = self.token.get_request_format()
        self.template_name = ("%s:" % format).split(':')[1]
        return format.startswith('template')
    
    def format(self):
        self.token.content_type = 'text/html'
        templates = internal_find( self.token.path, fields=["templates"] ).get("templates",{})
        if self.template_name == "":
            if self.token.slug == None:
                template = templates.get('detail')
            else: 
                template = templates.get('list')
        else:
            template = templates.get('%s' % self.template_name)
            
        print "%%%% templates: %r" % templates
        print "%%%% template: %r" % template
        print "%%%% response: %r" % {"response":self.token.response}
            
        self.token.response = pystache.render(template,response = self.token.response)