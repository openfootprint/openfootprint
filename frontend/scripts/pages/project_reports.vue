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
          <div class="icon-tab"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M3.71,16.29a1,1,0,0,0-.33-.21,1,1,0,0,0-.76,0,1,1,0,0,0-.33.21,1,1,0,0,0-.21.33,1,1,0,0,0,.21,1.09,1.15,1.15,0,0,0,.33.21.94.94,0,0,0,.76,0,1.15,1.15,0,0,0,.33-.21,1,1,0,0,0,.21-1.09A1,1,0,0,0,3.71,16.29ZM7,8H21a1,1,0,0,0,0-2H7A1,1,0,0,0,7,8ZM3.71,11.29a1,1,0,0,0-1.09-.21,1.15,1.15,0,0,0-.33.21,1,1,0,0,0-.21.33.94.94,0,0,0,0,.76,1.15,1.15,0,0,0,.21.33,1.15,1.15,0,0,0,.33.21.94.94,0,0,0,.76,0,1.15,1.15,0,0,0,.33-.21,1.15,1.15,0,0,0,.21-.33.94.94,0,0,0,0-.76A1,1,0,0,0,3.71,11.29ZM21,11H7a1,1,0,0,0,0,2H21a1,1,0,0,0,0-2ZM3.71,6.29a1,1,0,0,0-.33-.21,1,1,0,0,0-1.09.21,1.15,1.15,0,0,0-.21.33.94.94,0,0,0,0,.76,1.15,1.15,0,0,0,.21.33,1.15,1.15,0,0,0,.33.21,1,1,0,0,0,1.09-.21,1.15,1.15,0,0,0,.21-.33.94.94,0,0,0,0-.76A1.15,1.15,0,0,0,3.71,6.29ZM21,16H7a1,1,0,0,0,0,2H21a1,1,0,0,0,0-2Z"/></svg></div>
          <p>Reports</p>
        </template>

        <DataTable ref="table_main" :fields="reports_fields" collection="reports" :newitemtemplate='{}' />

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
                        <div class="template_selected_label"><span class="icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18.71,7.21a1,1,0,0,0-1.42,0L9.84,14.67,6.71,11.53A1,1,0,1,0,5.29,13l3.84,3.84a1,1,0,0,0,1.42,0l8.16-8.16A1,1,0,0,0,18.71,7.21Z"/></svg></span>Active</div>
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
import Vue from 'vue'

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

                    .icon svg {
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