//Facebook crap

FB.getLoginStatus(function(response){
	if(response.session){ // we are logged in!
		$.ajax({
			type: 'POST',
			url: '/login',
			data: {
				fb_id: response.session.uid
			},
			dataType: "json",
			success: function(data){
				if(data.status == "ok"){
                    window.location = "/";
                }
                else{
                    //no-op
                }
			}
		});
	} 
	else{



		FB.Event.subscribe('auth.login', function(response){
			if( response.status == "notConnected" || response.status == "unknown" ){
				window.location = "/";
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
							//alert("need f!");
							FB.api('/me/friends', function(friendResponse) {
								//alert(JSON.stringify(friendResponse));
								$.ajax({
									type: 'POST',
									url: '/create',
									data: {
										fb_id: response.session.uid,
										friendJson: JSON.stringify(friendResponse)
									},
                                    success: function(data){
                                        window.location = "/";
                                    }
								});
							});
						}
						else if(data.status == "ok"){
							window.location = "/";
						}
						else{
							alert("miss1!");
						}		
					},
					error: function(){
						alert("miss2!");
					}
				});

				$("#fb_info").empty();
				$("#fb_info").append("Hey you'z logged in!");
			}
		});
	}
});
