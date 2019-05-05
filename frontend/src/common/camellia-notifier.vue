<template>
	<div class="notifier" id="notifier">
		<div class="bs-docs-section">
			<div v-for="(msg, index) in msgs" class="row">
				<div class="col-lg-12 col-sm-12" v-if="msg.dismissible">
					<div class="bs-component">
						<div class="alert alert-dismissible"
									:class="{
									'alert-warning': msg.type=='warn',
									'alert-danger': msg.type=='error',
									'alert-success': msg.type=='success',
									'alert-info': msg.type=='info',
									}">
							<button type="button" class="close" data-dismiss="alert" @click="close(index)">×</button>
							<h4>{{ msg.title }}</h4>
							<p>{{ msg.msg }}</p>
						</div>
					</div>
				</div>
				<div class="col-lg-3 col-lg-3" v-if="!msg.dismissible">
				</div>
				<div class="col-lg-9 col-lg-9" v-if="!msg.dismissible">
					<div class="bs-component">
						<div class="alert alert-dismissible"
									:class="{
									'alert-warning': msg.type=='warn',
									'alert-danger': msg.type=='error',
									'alert-success': msg.type=='success',
									'alert-info': msg.type=='info',
									}">
							<button type="button" class="close" data-dismiss="alert" @click="close(index)">×</button>
							<p ><strong>{{ msg.title }}</strong> {{ msg.msg }}</p>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>


<script>

 var supported_types = [
	 'info',
	 'success',
	 'warn',
	 'error'
 ];
 
 export default {
	 name: 'camellia-notifier',
	 data() {
		 return {
			 msg_id: 0,
			 msgs: {}
		 }
	 },
	 methods: {
		 notify(type='info', title='', msg='', dismissible=false, timeout=3000){
			 if(supported_types.indexOf(type)<0){
				 type='error';
			 } 

			 if(msg.length > 256){
				 msg = msg.substr(0, 256) + ' ......';
			 }
			 this.msg_id = this.msg_id + 1;
			 var msg_id = 'msg-'+ this.msg_id;
			 this.$set(this.msgs, msg_id, {
				 type: type,
				 msg: msg,
				 title: title,
				 dismissible: dismissible
			 });

			 var self = this;
			 if(!dismissible){
				 setTimeout(function(){
					 self.close(msg_id);
				 }, timeout);
			 }
		 },
		 info(title, msg){
			 this.notify('info', title, msg, false, 3000);
		 },
		 success(title, msg){
			 this.notify('success', title, msg, false, 3000);
		 },
		 warn(title, msg){
			 this.notify('warn', title, msg, false, 10000);
		 },
		 error(title, msg){
			 this.notify('error', title, msg, false, 20000);
		 },
		 axios_error(error, title){
			 var msg='未知错误';
			 if(error.response){
				 if(typeof(error.response.data.msg)=='string'){
					 if(error.response.data.title){
						 msg = error.response.data.title + "  " + error.response.data.msg;
					 }else{
						 msg = error.response.data.msg;
					 }
				 }else{
					 msg = error.response.data.toString();
				 }
			 }else if(error.message){
				 msg = error.message;
			 }
			 this.error(title, msg);
		 },
		 close(index){
			 Vue.delete(this.msgs, index);
		 }

	 }
 }
</script>
