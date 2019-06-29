<template>
    <div v-if="!item">Loading...</div>
    <div v-else>
        <div class="btns_actions">
            <h2><b-link :to='{"name": "project_reports"}'>Reports</b-link> / {{item.name}}</h2>
            <div class="btns">
                <b-button>View report</b-button>
            </div>
            <div class="clearfix"></div>
        </div>



    </div>
</template>


<script>


import Vue from 'vue'

export default {
    computed: {
        item() {
            if (!this.$parent.project.reports) return {};
            var id = this.$route.params.report_id;
            for (var i=0;i<this.$parent.project.reports.length;i++) {
                if (this.$parent.project.reports[i].id == id) {
                    return this.$parent.project.reports[i];
                }
            }
        }
    }
}

</script>

<style lang="scss" scoped>
</style>