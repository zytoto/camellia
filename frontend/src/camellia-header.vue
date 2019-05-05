<template>
	<div class="navbar navbar-default navbar-fixed-top">
		<div class="container">
			<div class="navbar-header">
				<a href="/statics/user-info.html" class="navbar-brand" style="font-family: pacifico;font-size:22px;text-shadow: rgba(255,255,255,.5) 0 1px 8px;">
					<i class="camellia-icon icon-camellia" style="padding-right:5px;"></i>
					Camellia
				</a>

			</div>
			
			<div class="navbar-collapse collapse" style="float:right;">
				<ul class="nav navbar-nav">
					<li><a href="/statics/user-info.html">主页</a></li>
					<li><a @click="logout()">退出登录</a></li>
				</ul>
			</div>
		</div>
	</div>
</template>

<script>
 export default {
	 name: 'camellia-header',
	 props: {
		 showNav: {
			 type: Boolean,
			 default: true
		 },
		 backToLogin: {
			 type: Boolean,
			 default: true
		 },
		 LoginPath: {
			 type: String,
			 default: '/statics/login.html'
		 }
	 },
	 methods: {
		 logout(){
			 var url = '/api/v1/login';

			 var self=this;
			 axios.delete(url).then(function(resp){
			 }).catch(function(error){
			 }).finally(function(){
			 });

			 if(this.backToLogin){
				 window.location = this.LoginPath;
			 }else{
				 window.location.reload();
			 }
		 }
	 }
 }
</script>
