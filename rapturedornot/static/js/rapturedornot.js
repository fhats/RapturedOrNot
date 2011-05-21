//Facebook crap

FB.Event.subscribe('auth.login', function(response){
    if( response.status == "notConnected" || response.status == "unknown" ){
        return false;
    }
    else{
        //We got teh FBcksz!
        $.ajax({
            type: 'POST',
            url: '/login',
            data: {
                    fb_id: response.session.uid
                  },
            dataType: "json",
        });
        
        $("#fb_info").empty();
        $("#fb_info").append("Hey you'z logged in!");
    }
});