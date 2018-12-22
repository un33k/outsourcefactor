(function($){tile = function() {
    
    /* be focused, prefebly on the first text type input */
    $("input[type='text']:first", document.forms[0]).focus();
    
    /* let'm pick their dates the easy way */
    $('.vDateFieldAge').datepicker({ dateFormat: 'yy-mm-dd', changeYear: true, changeMonth: true, yearRange: '-60:-14'});
    $('.vDateFieldStartDate').datepicker({ dateFormat: 'yy-mm-dd', changeYear: true, changeMonth: true, minDate: '0'});
    $('.vDateFieldAvailableDate').datepicker({ dateFormat: 'yy-mm-dd', changeYear: true, changeMonth: true, minDate: '0'});
    
    /* ask twice delete once : */
    // $('.confirm').click(function(event){if(window.confirm("Are you sure?"))return false;});
    
    /* post simply rules */
    $('a.post_link').click(function () {
        if ($(this).hasClass('confirm')){
            if(!window.confirm("Are you sure?")){
                return false;
            }
        }
        $('#csrf_post_form').attr('action', this.href).submit();
        return false;
    });
    
    /* messages are great but get them out of my face slowly */
    // $('#msg_board').fadeOut(10000);

    /* if you select it (category), the skills (for that category) will come */
    $("select#id_skill_category").change(function(){
        csrf = $('#csrf_post_form').attr('class');
        url = $('#skill_add_get_subcat').attr('class');
        var postdata = {cat_id: $(this).val(), ajax: 'true', csrfmiddlewaretoken: csrf };
        $.post(url, postdata, function(data, status) {
            var options = '<option value="">---------</option>';
            for (var i = 0; i < data.length; i++) {
                options += '<option value="' + parseInt(data[i].id) + '">' + data[i].name + '</option>';
            }
            $("#id_skill_name").html(options);
            $("#id_skill_name option:first").attr('selected', 'selected');
            $("#id_skill_name").attr('disabled', false);
        }, "json");
    
      $("#id_skill_category").attr('selected', 'selected');
    });
  
    /* unless you select the category, you won't get anything (skill & experience leve) */
    if ($('#id_category').val() == "0"){
            $("#id_skill option:first").attr('selected', 'selected');
            $("#id_experience option:first").attr('selected', 'selected');
            $('#id_skill').attr('disabled', true);
            $('#id_experience').attr('disabled', true);
    }
    
    /* if you select the category, you get the skill & experience (enabled), no worries, you can go back */
    $("select#id_category").change(function(){
        csrf = $('#csrf_post_form').attr('class');
        url = $('#skill_search_get_subcat').attr('class');
        var postdata = {cat_id: $(this).val(), ajax: 'true', csrfmiddlewaretoken: csrf };
        $.post(url, postdata, function(data, status) {
            var options = '';
            for (var i = 0; i < data.length; i++) {
                options += '<option value="' + parseInt(data[i].id) + '">' + data[i].name + '</option>';
            }
            $("#id_skill").html(options);
            $("#id_skill option:first").attr('selected', 'selected');
        }, "json");
        if ($('#id_category').val() == "0"){
            $("#id_skill option:first").attr('selected', 'selected');
            $('#id_skill').attr('disabled', true);
            $("#id_experience option:first").attr('selected', 'selected');
            $('#id_experience').attr('disabled', true);
        } else {
            $('#id_skill').attr('disabled', false);
            $('#id_experience').attr('disabled', false);
        }   
    });
    // submit as soon as anything changes on the talent search form
    // make sure you send them to the url of the original form, not the pagination form
    $("#talent_search_form").change(function() {
        $(this).attr('action', this.href);
        $(this).submit();
        return false;
    });

    /* play a bit of accordion a day, keeps reloads away */
    $("#accordion").accordion({collapsible: true, autoHeight: false, active: false});
    
    /* watch videos with style */
    $('video').mediaelementplayer({features: ['playpause','loop','current','progress','duration','volume']});

    /* load email address per request */
    $('a.post_link_contact_info').click(function () {
        var csrf = $('#csrf_post_form').attr('class');
        var url = $('#profile_get_contact_info').attr('class');
        var user = $(this).attr('id');
        var postdata = { username: user, ajax: 'true', csrfmiddlewaretoken: csrf };
        $.post(url, postdata, function(data, status) {
            var email_link = 'mailto:'+data[0].email+'?subject=Contacting from [OSF]'
            anchorlink = $('#'+user)
            anchorlink.attr('href', email_link);
            anchorlink.hide();
            anchorlink.html(data[0].email);
            anchorlink.fadeIn(4000);
            anchorlink.unbind('click');
            anchorlink.removeClass('post_link_contact_info');  
            icon = anchorlink.siblings('span');
            icon.removeClass();  
            icon.addClass('email_to_icon');        
        }, "json");
        return false;
    });

    /* load job contact info (email or number) per request */
    $('a.post_link_job_contact_info').click(function () {
        var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        var csrf = $('#csrf_post_form').attr('class');
        var url = $('#employer_get_job_contact_info').attr('class');
        var jobid = $(this).attr('id');
        var postdata = { jobid: jobid, ajax: 'true', csrfmiddlewaretoken: csrf };
        $.post(url, postdata, function(data, status) {
            if(data[0].email.match(re)){
                var email_link = 'mailto:'+data[0].email+'?subject=Contacting from [OSF]'
                anchorlink = $('#'+jobid)
                anchorlink.attr('href', email_link);
                anchorlink.hide();
                anchorlink.html(data[0].email);
                anchorlink.fadeIn(4000);
                anchorlink.unbind('click');
                anchorlink.removeClass('post_link_job_contact_info');
            } else{
                block = $('#'+jobid)
                block.removeAttr('href');
                block.removeClass('employer_get_job_contact_info');
                block.unbind('click');
                block.hide();
                block.html(data[0].email);
                block.fadeIn(4000);
            }
        }, "json");
        return false;
    });


    /* if user is not logged in, they can't see contact info, send them to login page instead */
    $('a.login_required_or_signup').click(function () {
        $(this).hide();
        $(this).html('members only - signup for free');
        $(this).fadeIn(4000);
        $(this).unbind('click');
        $(this).removeClass('login_required_or_signup');
        return false;
    });
    
    // fadein fadeout affects
    $(".current-page-top").effect("highlight", {color:"#ff6600"}, 2000);
    
    // submit as soon as anything changes on the job search form
    // make sure you send them to the url of the original form, not the pagination form
    $("#job_search_form").change(function() {
        $(this).attr('action', this.href);
        $(this).submit();
        return false;
    });
    
    // submit as soon as anything changes on the business search form
    // make sure you send them to the url of the original form, not the pagination form
    $("#business_search_form").change(function() {
        $(this).attr('action', this.href);
        $(this).submit();
        return false;
    });
    
    
    /* from this job from bookmarks */
    function bookmark_toggler(event){
        
        var pk = $(this).attr('id');
        var obj = event.data.kind;
        if (event.data.action=='del'){
            var this_act = 'del'; 
            var next_act = 'add'; 
            var this_class = 'post_link_bookmark_'+obj+'_'+this_act;
            var next_class = 'post_link_bookmark_'+obj+'_'+next_act;
            var next_msg = 'add to favorites';
        } else if (event.data.action=='add'){
            var this_act = 'add'; 
            var next_act = 'del'; 
            var this_class = 'post_link_bookmark_'+obj+'_'+this_act;
            var next_class = 'post_link_bookmark_'+obj+'_'+next_act;
            var next_msg = 'remove from favorites';
        }
        
        var csrf = $('#csrf_post_form').attr('class');
        var url = $('#'+this_class).attr('class');
        var postdata = { pk: pk, ajax: 'true', csrfmiddlewaretoken: csrf };
        $.post(url, postdata, function(data, status) {
            if (data[0].bookmark_toggled == true){
                anchorlink = $('#'+pk)
                anchorlink.attr('href', $('#'+this_class).attr('href'));
                anchorlink.hide();
                anchorlink.html(next_msg);
                anchorlink.fadeIn(400);
                anchorlink.removeClass();  
                anchorlink.addClass(next_class);
                anchorlink.unbind('click')
                anchorlink.bind('click', {kind:obj, action:next_act}, bookmark_toggler);
                icon = anchorlink.siblings('span');
                icon.removeClass();  
                icon.addClass('favorites_icon_'+next_act);  
            }      
        }, "json");
        return false;
    };

    $('a.post_link_bookmark_profile_add').bind('click', {kind:'profile', action:'add'}, bookmark_toggler);
    $('a.post_link_bookmark_profile_del').bind('click', {kind:'profile', action:'del'}, bookmark_toggler);
        
    $('a.post_link_bookmark_job_add').bind('click', {kind:'job', action:'add'}, bookmark_toggler);
    $('a.post_link_bookmark_job_del').bind('click', {kind:'job', action:'del'}, bookmark_toggler);
    
};})(jQuery);