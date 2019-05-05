
var camellia = new Vue({
	el: "#camellia",
	data: {
		visible_page: 'product',
		popup_visible: null,
		dialoger: null,
		notifier: null,
		loader: null,
		user_info: {},
		users: [],
		page: 0,
		pagesize: 20,
		page_total: 1
	},
	methods: {
		init: function(){
			this.dialoger = this.$refs['dialoger'];
			this.notifier = this.$refs['notifier'];
			this.loader = this.$refs['loader'];

			if(typeof(my_info)=='undefined' || my_info.id=="None"){
				this.dialoger.confirm('', '您需要先登录才能访问该页面', function(){
					window.location = '/statics/login.html?orig='+Base64.encode(window.location.pathname+window.location.search);
				});
				return;
			}
			this.my_info = my_info;

			if(my_info.role != 0 && my_info.role != 1){
				this.dialoger.confirm('', '您无权访问该页面', function(){
					window.location='/statics/user-info.html?user_id='+my_info.id;
				});
			}

			this.get_user_list();
		},
		get_user_list: function(){
			var url = '/api/v1/user?mode=all&page='+this.page+'&pagesize='+this.pagesize;

			var self=this;
			self.loader.show('稍等');
			axios.get(url).then(function(resp){
				self.page_total = resp.data.page_total;
				self.users = resp.data.users;
			}).catch(function(error){
				self.notifier.axios_error(error, '获取用户列表失败:');
				if(error.response){
					if(error.response.status == 401){
						self.dialoger.ask('','您的登录已经超时，请重新登录.',function(){
							window.location = '/statics/login.html?orig='+Base64.encode(window.location.pathname+window.location.search);
						});
					}
				}
			}).finally(function(){
				self.loader.hide();
			});
		},
		get_user_page(page){
			if(page <= 0){
				page = 0;
			}
			if(page >= this.page_total){
				page = this.page_total - 1;
			}
			this.page = page;

			this.get_user_list();
		},
		get_user_next_page(){
			this.page = this.page + 1;
			if(this.page >= this.page_total){
				this.page = this.page_total -1;
			}
			this.get_user_list();
		},
		get_user_prev_page(){
			this.page = this.page - 1;
			if(this.page <= 0){
				this.page = 0;
			}
			this.get_user_list();
		},
		show_user(user_id){
			window.location='/statics/user-info.html?user_id='+user_id;
		}
	}
});

camellia.init();
