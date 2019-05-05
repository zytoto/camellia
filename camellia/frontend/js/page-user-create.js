
var camellia = new Vue({
	el: "#camellia",
	data: {
		visible_page: 'product',
		popup_visible: null,
		dialoger: null,
		notifier: null,
		loader: null,
		creator: {
			action: null,
			code: null,
			username: null,
			password: null,
			email: null,
			role: 2,
			gender: 1,
			avator: null,
			phone: null,
			description: null
		},
		form_state: {
			username: 0,
			email: 0,
			phone: 0,
			pass: 0
		},
		my_info: {
			role: 2
		},
	},
	methods: {
		init: function(){
			this.dialoger = this.$refs['dialoger'];
			this.notifier = this.$refs['notifier'];
			this.loader = this.$refs['loader'];

			var query = window.location.search.split('?');
			if(query.length > 1){
				var params = query[1].split('&');
				for(var i in params){
					var p = params[i].split('=');
					if(p[0]=='action'){
						this.creator.action = p[1];
					}else if(p[0]=='code'){
						this.creator.code = p[1];
					}
				}
			}

			if(typeof(my_info)=='undefined' || my_info.id=="None"){
			}else{
				if(this.creator.action == null){
					this.dialoger.confirm('', '您已登录，请先退出登录再开始注册.');
				}
				this.my_info = my_info;
			}
		},
		creat_user: function(){
			if(!this.form_check()){
				return;
			}
			var data = this.creator;
			
			var self=this;
			self.loader.show('稍等');
			axios.post('/api/v1/user', data).then(function(resp){
				if(self.creator.action==null){
					window.location = '/statics/login.html';
				}else{
					window.location = '/statics/user-info.html?id='+resp.data.user.id;
				}
			}).catch(function(error){
				self.notifier.axios_error(error, '创建用户失败:');
			}).finally(function(){
				self.loader.hide();
			});


			event.preventDefault();
			event.stopPropagation();
		},
		form_check(){
			var regMail = new RegExp("^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$");
			var regPhone = /^[1][3,4,5,7,8][0-9]{9}$/;
			var regName = /^[a-zA-Z0-9_-]{4,16}$/;
			// var regPass = /^.*(?=.{6,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*? ]).*$/;
			var regPass = /^.{6,32}/;

			var ret = true;
			if(!regMail.test(this.creator.email)){
				this.form_state.email = 1;
				this.notifier.error('无效的邮件地址，请输入正确的邮件地址.');
				ret = false;
			}else{
				this.form_state.email = 0;
			}

			if(!regName.test(this.creator.username)){
				this.form_state.username = 1;
				this.notifier.error('无效的用户名，用户名必须由字母数字和下划线组成，长度4-16位.');
				ret = false;
			}else{
				this.form_state.username = 0;
			}

			if(!regPhone.test(this.creator.phone)){
				this.form_state.phone = 1;
				this.notifier.error('无效的手机号码，请输入正确的手机号码.');
				ret = false;
			}else{
				this.form_state.phone = 0;
			}

			if(!regPass.test(this.creator.pass)){
				this.form_state.pass = 1;
				this.notifier.error('请输入6-32位长度的密码.');
				ret = false;
			}else{
				this.form_state.pass = 0;
			}

			return ret;
		}
	}
});

camellia.init();
