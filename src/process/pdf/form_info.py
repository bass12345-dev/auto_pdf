from src.process.query.query import input_query
import re
import json  

def query_rows():
     
    try:
       query = "select g_id ,g_name, g_link, g_category, mandatory from guidelines"
       result = input_query(query)
    except Exception as e:
        result = f"Query Error: {e}"

    return result

def find_word(word,string) :
    match = re.search(rf'\b{word}\b', string, re.IGNORECASE)
    return match

def form_process() :
    dict_list       = {}
    custom_list     = {}
    plugins         = []
    standards       = []
    after_effects   = []
    positioning_style = []
    fonts           = []
    title_style     = []
    title_effects   = []
    caption_style   = []
    caption_effects = []
    b_roll          = []
    b_roll_sourcing = []
    transitions     = []
    visuals         = []
    audio           = []
    custom          = []



    typography                  = []
    effect_stacks               = []
    ae_distort_effects          = []
    ae_perspective_effects      = []
    ae_blur_and_sharpen_effects = []
    ae_stylize_effects          = []
    ae_generated_effects        = []
    ae_distort                  = []
    caption_review              = []
    short_form                  = []
    others                      = []










    
    rows = query_rows()
    for row in rows:
        title = row[3]
        g_name = row[1]
        #Premiere Pro Plugins
        if(find_word('premiere pro plugins',title)):
            plugins.append(row)
        #Standard Frame Rate
        elif(find_word('standard frame',g_name)):
            standards.append(row)
        #After Effects
        elif(find_word('after effects plugins',title)):
            after_effects.append(row)
        #Positioning Style
        elif(find_word('Positioning Style',title)):
            positioning_style.append(row)
        #Title and Caption Fonts
        elif(find_word('fonts',title)):
            fonts.append(row)
        #Title Style
        elif(find_word('title style',title)):
            title_style.append(row)
        #Title Effects
        elif(find_word('title effects',title)):
            title_effects.append(row)

        #Caption Style
        elif(find_word('captions style',title)):
            caption_style.append(row)
        #Caption Effects
        elif(find_word('caption effects',title)):
            caption_effects.append(row)
        #B Roll System
        elif(find_word('b-roll system',title)):
            b_roll.append(row)
        #B Roll Sourcing
        elif(find_word('b-roll sourcing',title)):
            b_roll_sourcing.append(row)
        #Transitions
        elif(find_word('Transition Standards',title) or find_word('Premiere Composer',title)):
            transitions.append(row)
        #Visuals
        elif(find_word('visuals',title)):
            visuals.append(row)
        elif(find_word('Standard Audio',title)):
            audio.append(row)
        else:
            # row_custom = get_custom(row,title)
            # custom.append(row_custom)

            #Typography
            if(find_word('Typography Add-Ons',title)):
                typography.append(row)
            #Effect Stacks
            elif(find_word('Effect Stacks',title)):
                effect_stacks.append(row)
            #AE Distort Effects
            elif(find_word('AE Distort Effects',title)):
                ae_distort_effects.append(row)
            #AE Perspective Effects
            elif(find_word('AE Perspective Effects',title)):
                ae_perspective_effects.append(row)
            #AE Blur & Sharpen Effects
            elif(find_word('AE Blur & Sharpen Effects',title)):
                ae_blur_and_sharpen_effects.append(row)
            #AE Blur & Sharpen Effects
            elif(find_word('AE Stylize Effects',title)):
                ae_stylize_effects.append(row)    
            #AE Blur & Sharpen Effects
            elif(find_word('AE Stylize Effects',title)):
                ae_stylize_effects.append(row)    
            #AE Generate Effects
            elif(find_word('AE Generate Effects',title)):
                ae_generated_effects.append(row)    
            #AE Distort
            elif(find_word('AE Distort',title)):
                ae_distort.append(row)  
            #Caption Review
            elif(find_word('Caption Review',title)):
                caption_review.append(row)    
            #Short-Form Titles
            elif(find_word('Short-Form Titles',title)):
                short_form.append(row)  
            else:
                others.append(row)  

            custom_list['Titles']                         = others
            custom_list['Typography Add-Ons']                     = typography
            custom_list['Effect Stacks']                  = effect_stacks
            custom_list['AE Distort Effects']             = ae_distort_effects
            custom_list['AE Perspective Effects']         = ae_perspective_effects
            custom_list['AE Blur And Sharpen Effects']    = ae_blur_and_sharpen_effects
            custom_list['AE Stylize Effects']             = ae_stylize_effects          
            custom_list['AE Generate Effects']           = ae_generated_effects
            custom_list['AE Distort']                     = ae_distort
            custom_list['Caption Review']                 = caption_review
            custom_list['Short Form Titles']                     = short_form
            




    dict_list['premier_plugins']    = plugins
    dict_list['effects_plugins']    = after_effects
    dict_list['standards']          = standards
    dict_list['positioning_style']  = positioning_style
    dict_list['fonts']              = fonts
    dict_list['title_style']        = title_style
    dict_list['title_effects']      = title_effects
    dict_list['caption_style']      = caption_style
    dict_list['caption_effects']    = caption_effects
    dict_list['b_roll_guide']       = b_roll
    dict_list['b_roll_sourcing']    = b_roll_sourcing
    dict_list['transitions']        = transitions
    dict_list['visuals']            = visuals
    dict_list['audio']              = audio
    dict_list['custom']             = custom_list

    # json_object     = json.dumps(dict_list['custom'], indent = 4) 
    # print(json_object)
    return dict_list



    
    