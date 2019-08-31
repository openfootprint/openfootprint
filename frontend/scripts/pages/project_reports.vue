<template>
  <div>
    <div>
      <h2>Reports</h2>
    </div>


    <div class="report_list">

        <b-card v-for="report in project.reports" :key="report.id">
          <b-card-text>
            <b-link :to="{ name: 'project_report', params: { report_id: report.id } }">{{report.name}}</b-link>
          </b-card-text>
        </b-card>

    </div>

    <br/>

    <b-button v-b-modal.modal-template>
      New report
    </b-button>

    <b-modal
      id="modal-template"
      ref="modal_template"
      scrollable
      size="xl"
      title="Please select a theme"
    >
      <div class="row template_list">

        <article @click="selectTheme(plugin)" v-for="plugin in available_themes" :key="plugin.slug" class="col-lg-4">
          <div class="template_block">
            <div class="template_preview">
              <img src="/openfootprint/templates/reports/event1/preview.jpg" />
            </div>
            <div class="template_details">
              <p>{{plugin.name}}</p>
            </div>
            <!--<div class="template_selected_label">Active</div>-->
          </div>
        </article>
      </div>
    </b-modal>

  </div>
</template>

<script>
import DataTable from "../components/datatable";

export default {
  components: {
    DataTable
  },
  data() {
    return {
      reports_fields: [
        {
          key: "name",
          label: "Name"
        },
        {
          key: "report_template",
          label: "Template"
        },
        {
          key: "report_date",
          label: "Date"
        },
        {
          key: "actions",
          label: "",
          class: "th_actions"
        }
      ]
    };
  },
  computed: {
    available_themes() {
      var themes = [];
      (this.project.plugins||[]).forEach((plugin) => {
        if (plugin.type == "theme") {
          themes.push(plugin);
        }
      });
      return themes;
    }
  },
  methods: {
    selectTheme(plugin) {
      this.loading_save = true;
      this.project.reports.push({
        name: "New report",
        theme_slug: plugin.slug
      });
      this.$http
        .post(this.project_api_root + "/set_reports", this.project.reports)
        .then(() => {
          this.refreshProject(() => {
            this.loading_save = false;
            this.$router.push("reports/" + this.project.reports[this.project.reports.length-1]["id"]);
          });
        });
    }
  }
};
</script>

<style lang="scss" scoped>
.template_list {
  .template_block {
    border: 1px solid $gray-200;
    border-radius: 8px;
    overflow: hidden;
    cursor: pointer;

    .template_preview {
      background-color: #000;
      margin-left: -15px;
      margin-right: -15px;
      min-height: 200px;

      img {
        width: 100%;
        height: auto;
        background-color: #000;
      }
    }

    .template_details {
      background-color: #fff;
      padding: 15px 20px;
      position: relative;

      p {
        font-weight: bold;
        margin: 0px;
      }
    }
    &:hover .template_details .icon {
      display: block;
      &:hover {
        svg {
          fill: $gray-700;
        }
      }
    }
  }

  .template_selected {
    .template_block {
      border: 1px solid $green;
      position: relative;

      .template_selected_label {
        background-color: $green;
        color: #fff;
        position: absolute;
        top: 20px;
        right: 0px;
        padding: 3px 10px;
        font-size: 14px;
        border-top-left-radius: 8px;
        border-bottom-left-radius: 8px;

        svg {
          width: 20px;
          margin-right: 3px;
          fill: #fff;
        }
      }
    }
  }
}

.tab_help {
  padding-bottom: 10px;
}
</style>
