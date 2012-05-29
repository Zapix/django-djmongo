from django.contrib import admin


class NoSqlModelAdmin(admin.ModelAdmin):
    change_form_template = 'admin/nosql/form_change.html'
    add_form_template = 'admin/nosql/form_change.html'

    mongo_classes = ""
    mongo_name = ""
    mongo_description = ""

    def get_mongo_form_class(self, obj=None):
        '''
        Gets mongo form class for current obj
        '''
        raise NotImplementedError

    def get_mongo_initial(self, obj=None):
        '''
        Return's initial data for mongo
        '''
        return obj.document if obj else {}

    def get_mongo_form_kwargs(self, obj=None):
        '''
        Returns kwargs for mongo document
        '''
        return {'initial': self.get_mongo_initial(obj)}

    def get_mongo_form(self, obj=None):
        '''
        Generates form for document
        :param obj: Object with document
        :return: Builded form or None
        '''
        try:
            form_class = self.get_mongo_form_class(obj)

            # if it's none
            if form_class is None:
                return None

            return form_class(prefix="mongo",
                              **self.get_mongo_form_kwargs(obj))
        except NotImplementedError:
            return None

    def render_change_form(self, request, context, add=False,
                           change=False, form_url='', obj=None):
        '''
        Adds mongo form into context
        '''
        mongo_form = self.get_mongo_form(obj)
        context.update({'mongo_form': mongo_form,
                        'mongo_classes': self.mongo_classes,
                        'mongo_name': self.mongo_name,
                        'mongo_description': self.mongo_description})
        return super(NoSqlModelAdmin, self).render_change_form(
                                                request,
                                                context,
                                                add,
                                                change,
                                                form_url,
                                                obj)

