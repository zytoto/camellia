
var camellia = new Vue({
	el: "#camellia",
	data: {
		visible_page: 'product',
		popup_visible: null,
		dialoger: null,
		notifier: null,
		loader: null
	},
	methods: {
		init: function(){
			this.dialoger = this.$refs['dialoger'];
			this.notifier = this.$refs['notifier'];
			this.loader = this.$refs['loader'];

		},
		get_clusters(){
			this.$refs['cluster-list-main'].get_clusters();
		},
		change_cluster_attr(msg){
			this.$refs['cluster-list-main'].change_cluster_attr(msg);
		}
	}
});

camellia.init();
