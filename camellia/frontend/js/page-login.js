var camellia = new Vue({
	el: "#camellia",
	data: {
		username: null,
		password: null
		
	},
	methods: {
		init: function(){
			this.dialoger = this.$refs['dialoger'];
			this.notifier = this.$refs['notifier'];
			this.loader = this.$refs['loader'];

		},
		login(event){
			if(this.username == null || this.password == null){
				this.notifier.error('', '请填写用户名密码');
				return;
			}
			var data = {
				username: this.username,
				password: this.password,
				query: window.location.search.substr(1)
			};
			
			var self=this;
			self.loader.show('稍等');
			axios.post('/api/v1/login', data).then(function(resp){
				window.location = resp.data.orig;
			}).catch(function(error){
				self.notifier.axios_error(error, '登录失败:');
			}).finally(function(){
				self.loader.hide();
			});


			event.preventDefault();
			event.stopPropagation();
		},
		focus_in(){
			this.$refs.inputUsername.focus();
		}
	}
});

camellia.init();
camellia.focus_in();
