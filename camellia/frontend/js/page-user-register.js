
var camellia = new Vue({
	el: "#camellia",
	data: {
		visible_page: 'product',
		popup_visible: null,
		dialoger: null,
		notifier: null,
		loader: null,
		creator: {
			username: null,
			password: null,
			email: null,
			role: 2,
			gender: 1,
			avator: null,
			phone: null,
			description: null
		},
		my_info: {
			role: 2
		}
	},
	methods: {
		init: function(){
			this.dialoger = this.$refs['dialoger'];
			this.notifier = this.$refs['notifier'];
			this.loader = this.$refs['loader'];

			if(typeof(my_info)=='undefined' || my_info==null){
				this.dialoger.confirm('', '您需要先登录才能访问该页面', function(){
					window.location = '/statics/login.html';
				});
				return;
			}
			this.my_info = my_info;
		},
		creat_user: function(){
			var data = this.creator;
			
			var self=this;
			self.loader.show('稍等');
			axios.post('/api/v1/user', data).then(function(resp){
				window.location = '/statics/user-info.html?id='+resp.data.user.id;
			}).catch(function(error){
				self.notifier.axios_error(error, '创建用户失败:');
			}).finally(function(){
				self.loader.hide();
			});


			event.preventDefault();
			event.stopPropagation();
		}
	}
});

camellia.init();
