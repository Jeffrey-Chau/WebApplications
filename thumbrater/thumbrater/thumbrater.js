(function(){
	var thumbrater = {
		props: ['url', 'callback_url'],
		data: null,
		methods: {},
	};

	thumbrater.data = function(){
		var data = {
			rating: 0,
			get_url: this.url,
			set_url:  this.callback_url,
		};
		thumbrater.methods.load.call(data);
		return data;
	};

	thumbrater.methods.set_thumb_rating = function (rating) {
		let self = this;
		console.log("self.rating: ",self.rating)
		console.log("Setting rating ",rating)
		axios.get(self.set_url, {
			params: {
				rating: rating
			}}).then(function(res) {
				console.log(self)
				if (self.rating == rating){
					console.log("inside if")
					self.rating = 0;
				} else {
					self.rating = rating;
				}
			});

	};

	thumbrater.methods.load = function(){
		let self = this;
		axios.get(self.get_url)
			.then(function(res) {
				self.rating = res.data.rating;
			});
	};

	utils.register_vue_component("thumbrater", "components/thumbrater/thumbrater.html",
		function (template) {
			thumbrater.template = template.data;
			return thumbrater;
		});

})();
