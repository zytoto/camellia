<template>
	<div class="dialog" id="dialog">
		<div class="popup" :class="{visible:(popup_visible=='ask')}">
			<div class="bs-docs-section popup-content" :class="{visible:(popup_visible=='ask')}" style="min-width:20%;width:40%;left:30%;min-height:10%;padding-bottom:1em;">
				<div class="row">
					<div class="col-lg-12">
						<p>{{ msg }}</p>
					</div>
				</div>
				<div class="row">
					<div class="col-lg-12" style="text-align:right;">
						<a href="#" class="btn btn-primary" @click="_do_confirm()">确认</a>	
						<a v-if="type=='ask'" href="#" class="btn btn-default" @click="popup_visible=null;">取消</a>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
 export default {
	 name: 'camellia-dialoger',
	 data(){
		 return {
			 type: 'ask',
			 title: null,
			 msg: null,
			 callback: null,
			 data: null,
			 popup_visible: null
		 };
	 },
	 methods: {
		 ask(title, msg, callback, data){
			 this.type='ask';
			 this.title=title;
			 this.msg=msg;
			 this.callback=callback;
			 this.data=data;
			 this.popup_visible='ask';
		 },
		 confirm(title, msg, callback, data){
			 this.type='confirm';
			 this.title=title;
			 this.msg=msg;
			 this.callback=callback;
			 this.data=data;
			 this.popup_visible='ask';
		 },
		 _do_confirm(){
			 if(this.callback){
				 this.callback(this.data);
			 }
			 this.popup_visible=null;
		 }
	 }
 }
</script>

<style scoped>
 .dialog{
	 position: fixed;
	 z-index: 2002;
 }
</style>
