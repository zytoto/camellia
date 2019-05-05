<template>
	<div class="loader" v-show="loader_global!=null"> 
		<div class="loader-container" v-if="loader_global=='spinner'">
			<div class="loader-icon">
				<i class="fa fa-spinner fa-spin fa-fw" style="font-size:240px;color:#333;"></i>
			</div>
			<div class="loader-title" v-if="title!=null">
				{{ title }} ...
			</div>
		</div>

	</div>
</template>

<script>

 var supported_types = [
	 'spinner'
 ];

 export default {
	 name: 'camellia-loader',

	 data(){
		 return {
			 title: null,
			 loader_global: null
		 }
	 },
	 methods: {
		 show(title, type){
			 this.title = title;

			 var type_index = supported_types.indexOf(type);
			 if(type_index == -1){
				 type_index = parseInt(Math.random()*100%supported_types.length);
			 }
			 type = supported_types[type_index];
			 this.loader_global = type;
		 },
		 hide(){
			 this.loader_global = null;
		 }
	 }
 }
</script>

<style scoped>

 .loader{
	 position: fixed;
	 z-index: 2101;
	 top: 0px;
     width: 100%;
	 height: 100%;
     right: 0px;
	 background-color: #00000080;
 }

 .loader > .loader-container{
	 width: 370px;
	 margin: auto;
	 margin-top: 75px;
	 border-radius: 5px;
	 text-align: center;
	 padding:30px;
	 background-color: white;
 }

 .loader > .loader-container > .loader-icon{
	 text-align: center;
 }

 .loader > .loader-container > .loader-title{
	 text-align:center;
	 margin-top:30px;
	 font-size: 30px;
	 font-weight: bold;
 }

</style>
