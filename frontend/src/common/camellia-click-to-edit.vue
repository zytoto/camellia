<template>
	<div class="col-lg-12 col-sm-12">
		<form class="c-to-editor" @submit="change($event)">
			<div v-show="!on_edit">
				<h1  v-if="type=='h1'" :class="face">{{ orig }} <i class="fa fa-edit fa-lg" @mouseup="show_editor()"></i></h1>
				<h2  v-if="type=='h2'" :class="face">{{ orig }} <i class="fa fa-edit fa-lg" @mouseup="show_editor()"></i></h2>
				<h3  v-if="type=='h3'" :class="face">{{ orig }} <i class="fa fa-edit fa-lg" @mouseup="show_editor()"></i></h3>
				<h4  v-if="type=='h4'" :class="face">{{ orig }} <i class="fa fa-edit fa-lg" @mouseup="show_editor()"></i></h4>
				<h5  v-if="type=='h5'" :class="face">{{ orig }} <i class="fa fa-edit fa-lg" @mouseup="show_editor()"></i></h5>
				<h6  v-if="type=='h6'" :class="face">{{ orig }} <i class="fa fa-edit fa-lg" @mouseup="show_editor()"></i></h6>
				<span  v-if="type=='span'" :class="face">{{ orig }} <i class="fa fa-edit fa-lg" @mouseup="show_editor()"></i></span>
				<p  v-if="type=='p'" :class="face">{{ orig }} <i class="fa fa-edit fa-lg" @mouseup="show_editor()"></i></p>
				<label  v-if="type=='label'" :class="face">{{ orig }} <i class="fa fa-edit fa-lg" @mouseup="show_editor()"></i></label>
			</div>

			<div v-show="on_edit" class="input-group" 
				 @focusout="cancel()">
				<input
					class="c-to-editor form-control"
					v-model="target"
					ref="editor"/>
				<span class="input-group-btn">
					<button class="btn btn-primary" type="button" @mousedown="change($event)">确认</button>
				</span>
			</div>
		</form>
	</div>
</template>

<script>
 export default {
	 name: 'camellia-click-to-edit',
	 props: {
		 text: {
			 type: String,
			 default: ''
		 },
		 type: {
			 type: String,
			 default: 'h1'
		 },
		 face: {
			 type: String,
			 default: ''
		 }
	 },
	 data(){
		 return {
			 on_edit: false,
			 orig: this.text,
			 target: this.text
		 };
	 },
	 methods: {
		 show_editor: function(){
			 this.on_edit = true;
			 this.$nextTick( () => {
				 this.$refs.editor.focus();
			 });
		 },
		 cancel: function(){
			 this.on_edit = false;
			 this.target = this.orig;
		 },
		 change: function($event){
			 this.orig = this.target;
			 this.on_edit = false;
			 $event.preventDefault();
			 this.$emit('change', this.target);
		 }
	 }
 }
</script>
