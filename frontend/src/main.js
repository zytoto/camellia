import camelliaHeader from './camellia-header.vue';
import camelliaClickToEdit from './common/camellia-click-to-edit.vue';
import camelliaDialoger from './common/camellia-dialoger.vue';
import camelliaLoader from './common/camellia-loader.vue';
import camelliaNotifier from './common/camellia-notifier.vue';



const camelliacomponents = {
    install(Vue, options) {
        Vue.component(camelliaHeader.name, camelliaHeader);
        Vue.component(camelliaClickToEdit.name, camelliaClickToEdit);
        Vue.component(camelliaDialoger.name, camelliaDialoger);
        Vue.component(camelliaLoader.name, camelliaLoader);
        Vue.component(camelliaNotifier.name, camelliaNotifier);
	}
};

if( typeof window !== 'undefined' && window.Vue){
	window.Vue.use(camelliacomponents);
}

export default camelliacomponents;
