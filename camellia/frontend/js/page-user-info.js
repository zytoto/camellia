
var camellia = new Vue({
	el: "#camellia",
	data: {
		visible: 'contribute',
		popup_visible: null,
		dialoger: null,
		notifier: null,
		loader: null,
		my_info: {},
		invite_prefix: '',
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

			this.invite_prefix = 'http://'+window.location.host+'/statics/user-create.html?code=';

			if(typeof(my_info)=='undefined' || my_info.id=="None"){
				this.dialoger.confirm('', '您需要先登录才能访问该页面', function(){
					window.location = '/statics/login.html?orig='+Base64.encode(window.location.pathname+window.location.search);
				});
				return;
			}
			this.my_info = my_info;

			var query = window.location.search.split('?');
			var user_id = my_info.id;
			if(query.length > 1){
				var params = query[1].split('&');
				for(var i in params){
					var p = params[i].split('=');
					if(p[0]=='user_id'){
						user_id = p[1];
					}
				}
			}
			this.get_user_info(user_id);

		},
		get_user_info(user_id){
			var url = '/api/v1/user/'+user_id+'/detail';

			var self=this;
			self.loader.show('稍等');
			axios.get(url).then(function(resp){
				self.user_info = resp.data.user;
				self.get_user_list();
			}).catch(function(error){
				self.notifier.axios_error(error, '获取用户信息失败:');
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
		get_user_list: function(){
			var url = '/api/v1/user?mode=self&page='+this.page+'&pagesize='+this.pagesize+'&user_id='+this.user_info.id;

			var self=this;
			self.loader.show('稍等');
			axios.get(url).then(function(resp){
				self.page_total = resp.data.page_total;
				self.users = resp.data.users;
			}).catch(function(error){
				self.notifier.axios_error(error, '获取用户列表失败:');
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
