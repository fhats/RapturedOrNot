//Facebook crap

FB.Event.subscribe('auth.login', function(response){
    alert(response.status);
    if( response.status == "notConnected" || response.status == "unknown" ){
        alert("Not logged in!!");
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
			success: function(data){
				if(data.status == "error" && data.needs == "friends"){
					FB.api('/me/friends', function(friendResponse) {
						alert(friendResponse.data);
					});
				}
				else if(data.status == "ok"){
					FB.api('/me/picture',{type: large}, function(response){
						alert();
					});
				}		
			}
        });

        $("#fb_info").empty();
        $("#fb_info").append("Hey you'z logged in!");
    }
});