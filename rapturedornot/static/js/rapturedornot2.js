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
						alert(JSON.stringify(friendresponse));
                        /*$.ajax({
                        	
                        
                        })*/
					});
				}
				else if(data.status == "ok"){
					var requestURL = "/";
					requestURL.append(data.friendUID);
					requestURL.append("/picture");
					FB.api(requestURL,{type: "large"}, function(response){
						alert(response);
					});
				}
				else{
					alert("miss!");
				}		
			}
        });

        $("#fb_info").empty();
        $("#fb_info").append("Hey you'z logged in!");
    }
});