<template>
  <div>
    <div class="btns_actions">
      <h2>Reports</h2>
      <div class="btns">
        <b-button v-b-modal.modal-template>New report</b-button>
      </div>
      <div class="clearfix"></div>
    </div>

    <b-tabs>

      <b-tab active>
        <template slot="title">
          <div class="icon-tab"><unicon name="list-ul"></unicon></div>
          <p>Reports</p>
        </template>

        <DataTable ref="table_main" :fields="reports_fields" collection="reports" :newitemtemplate='{"name": "New report"}' />

        <b-modal id="modal-template" scrollable size="xl" ref="modal_template" title="Please select a template">
            <p>Help text if needed</p>
            <div class="row template_list">
                <article class="col-lg-4 template_selected">
                    <div class="template_block">
                        <div class="template_preview">
                            <img src="/openfootprint/templates/reports/event1/preview.jpg" />
                        </div>
                        <div class="template_details">
                            <p>Template name</p>
                        </div>
                        <div class="template_selected_label"><unicon name="check"></unicon>Active</div>
                    </div>
                </article>

                <article class="col-lg-4">
                    <div class="template_block">
                        <div class="template_preview">
                            <img src="/openfootprint/templates/reports/event1/preview.jpg" />
                        </div>
                        <div class="template_details">
                            <p>Template name</p>
                        </div>
                    </div>
                </article>

                <article class="col-lg-4">
                    <div class="template_block">
                        <div class="template_preview">
                            <img src="/openfootprint/templates/reports/event1/preview.jpg" />
                        </div>
                        <div class="template_details">
                            <p>Template name</p>
                        </div>
                    </div>
                </article>
            </div>
        </b-modal>

      </b-tab>
    </b-tabs>

  </div>
</template>


<script>

import DataTable from "../components/datatable"

export default {
  data () {
    return {
      reports_fields: [
        {
          "key": "name",
          "label": "Name"
        },
        {
          "key": "report_template",
          "label": "Template"
        },
        {
          "key": "report_date",
          "label": "Date"
        },
        {
          "key": "actions",
          "label": "",
          "class": "th_actions"
        }
      ]
    };
  },
  mounted() {
  },
  methods: {

  },
  components: {
    DataTable
  }
}
</script>

<style lang="scss" scoped>
    .template_list {
        .template_block {
            border:1px solid $gray-200;
            border-radius: 8px;
            overflow: hidden;
            cursor: pointer;

            .template_preview {
                background-color:#000;
                margin-left:-15px;
                margin-right:-15px;
                min-height: 200px;

                img {
                    width:100%;
                    height:auto;
                    background-color:#000;
                }
            }

            .template_details {
                background-color:#FFF;
                padding:15px 20px;
                position: relative;

                p {
                    font-weight: bold;
                    margin:0px;
                }
            }
            &:hover .template_details .icon {
                display: block;
                &:hover {
                    svg {
                        fill:$gray-700;
                    }
                }
            }
        }

        .template_selected {
            .template_block {
                border:1px solid $green;
                position: relative;

                .template_selected_label {
                    background-color:$green;
                    color:#FFF;
                    position: absolute;
                    top:20px;
                    right:0px;
                    padding:3px 10px;
                    font-size:14px;
                    border-top-left-radius: 8px;
                    border-bottom-left-radius: 8px;

                    svg {
                        width:20px;
                        margin-right:3px;
                        fill:#FFF;
                    }
                }
            }
        }
    }

    .tab_help {
        padding-bottom:10px;
    }

</style>