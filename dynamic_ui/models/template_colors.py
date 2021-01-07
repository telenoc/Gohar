from odoo import models, fields, api, _
import base64


class TemplateColors(models.TransientModel):
    _name = "template.colors"
    _description = 'Color Picker'

    SCSS_TEMPLATE = """
          
        body {{
             color: {basic_text_color};
           }}

       .o_main_navbar > a:hover, .o_main_navbar > a:focus, .o_main_navbar > button:hover, .o_main_navbar > button:focus
       {{
           background-color: {navi_hover} !important;
       
       }}
       .o_main_navbar > ul > li > a:hover, .o_main_navbar > ul > li > label:hover
       {{
           background-color: {navi_hover} !important;
       
       }}
       .o_main_navbar > ul > li > a:hover, .o_main_navbar > ul > li > label:hover
       {{
           color: {navi_hover_fontcolor} !important;
       
       }}

       .o_main_navbar {{
             background-color: {navi_background} !important;
             color: {navi_fontcolor} !important;
           }}
        
      .o_list_view .o_list_table thead{{
             background-color: {navi_background} !important;
             color: {navi_fontcolor} !important;
           }}
      .o_list_view .o_list_table tfoot
      {{
             background-color: {navi_background} !important;
             color: {navi_fontcolor} !important;
           }}         
            
       .o_main_navbar > ul > li > a, .o_main_navbar > ul > li > label
       {{
             color: {navi_fontcolor} !important;
           }}
       
       .btn-primary {{
            color: {btn_primary_fontcolor};
            background-color: {btn_primary_background};
        }}
        
        .o_home_menu_background
        {{
          
          background:{home_background}!important;
        }}
    """

    URL = '/dynamic_ui/static/src/scss/colors.scss'

    navi_background = fields.Char(string="Navigation Background",default="")
    basic_text_color = fields.Char(string="Basic Text Color",default="")
    navi_fontcolor = fields.Char(string="Navigation Fontcolor",default="")
    navi_hover = fields.Char(string="Navigation Hover Background",default="")
    navi_hover_fontcolor = fields.Char(string="Navigation Hover Font",default="")
    btn_primary_background = fields.Char(string="Button Backgroundcolor",default="")
    btn_primary_fontcolor = fields.Char(string="Button Fontcolor",default="")
    home_background = fields.Char(default="")





    def execute(self):
        self.env['ir.config_parameter'].set_param("navi_background", self.navi_background)
        self.env['ir.config_parameter'].set_param("home_background",self.home_background)
        self.env['ir.config_parameter'].set_param("navi_fontcolor", self.navi_fontcolor)
        self.env['ir.config_parameter'].set_param("navi_hover", self.navi_hover)
        self.env['ir.config_parameter'].set_param("navi_hover_fontcolor", self.navi_hover_fontcolor)
        self.env['ir.config_parameter'].set_param("basic_text_color", self.basic_text_color)
        self.env['ir.config_parameter'].set_param("btn_primary_background", self.btn_primary_background)
        self.env['ir.config_parameter'].set_param("btn_primary_fontcolor", self.btn_primary_fontcolor)
        self.scss_dynamic_attachment()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }



    @api.model
    def default_get(self, fields):
        if self.env['ir.config_parameter'].get_param("home_background"):
            home_background = self.env['ir.config_parameter'].get_param("home_background")
        else:
            home_background = ''

        if self.env['ir.config_parameter'].get_param("navi_background"):
            navi_background = self.env['ir.config_parameter'].get_param("navi_background")
        else:
            navi_background = ''

        if self.env['ir.config_parameter'].get_param("navi_fontcolor"):
            navi_fontcolor = self.env['ir.config_parameter'].get_param("navi_fontcolor")
        else:
            navi_fontcolor = '#FFFFFF'

        if self.env['ir.config_parameter'].get_param("navi_hover"):
            navi_hover = self.env['ir.config_parameter'].get_param("navi_hover")
        else:
            navi_hover = '#FFFFFF'

        if self.env['ir.config_parameter'].get_param("navi_hover_fontcolor"):
            navi_hover_fontcolor = self.env['ir.config_parameter'].get_param("navi_hover_fontcolor")
        else:
            navi_hover_fontcolor = '#1E2C52'

        if self.env['ir.config_parameter'].get_param("basic_text_color"):
            basic_text_color = self.env['ir.config_parameter'].get_param("basic_text_color")
        else:
            basic_text_color = '#141414'

        if self.env['ir.config_parameter'].get_param("btn_primary_background"):
            btn_primary_background = self.env['ir.config_parameter'].get_param("btn_primary_background")
        else:
            btn_primary_background = '#374D8B'

        if self.env['ir.config_parameter'].get_param("btn_primary_fontcolor"):
            btn_primary_fontcolor = self.env['ir.config_parameter'].get_param("btn_primary_fontcolor")
        else:
            btn_primary_fontcolor = '#FFFFFF'

        res = {
            "home_background":home_background,
            "navi_background":navi_background,
            "navi_fontcolor":navi_fontcolor,
            "navi_hover":navi_hover,
            "navi_hover_fontcolor":navi_hover_fontcolor,
            "basic_text_color":basic_text_color,
            "btn_primary_background":btn_primary_background,
            "btn_primary_fontcolor":btn_primary_fontcolor
        }
        return res

    def scss_dynamic_attachment(self):
        IrAttachmentObjects = self.env['ir.attachment']
        parameters = self.sudo().default_get([])
        css_data = self.SCSS_TEMPLATE.format(**parameters)
        datas = base64.b64encode(css_data.encode('utf-8'))
        customized_attachment = IrAttachmentObjects.sudo().search([('url', 'like', self.URL)])
        values = {
            'datas': datas,
            'url': self.URL,
            'name': self.URL,
        }
        if customized_attachment:
            customized_attachment.sudo().write(values)
        else:
            values.update({
                'type': 'binary',
                'mimetype':'text/scss',
            })
            IrAttachmentObjects.sudo().create(values)
        self.env['ir.qweb'].sudo().clear_caches()
        return self.URL



