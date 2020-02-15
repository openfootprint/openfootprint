<template>
  <div :class="'status-' + ((value || {}).status || 'empty')">
    <!-- {{(value||{}).country}} -->
    <b-input
      :value="(value || {}).source_name || ''"
      @input="onInput"
      :placeholder="placeholder || ''"
      data-lpignore="true"
    />
  </div>
</template>

<script>
export default {
  props: ["value", "placeholder"],
  methods: {
    onInput(value) {
      this.$emit("input", { source_name: value });
    }
  }
};
</script>

<style lang="scss" scoped>
input {
  padding-left: 30px;
}

.datatable_block.locations {
  .table thead th.th_actions {
    width: 64px;
  }

  .status-empty,
  .status-new,
  .status-geocoded,
  .status-unknown {
    position: relative;

    input {
      padding-left: 20px;
      margin-right: -20px;
    }

    &:before {
      content: "";
      background-position: left 0px center;
      background-size: 16px;
      display: inline-block;
      position: absolute;
      left: 0px;
      top: 0px;
      width: 19px;
      height: 21px;
    }
  }

  .status-new {
    input {
      border-bottom: 1px solid $gray2 !important;
    }

    &:before {
      animation: bounceMarker 2s infinite;
    }

    &::after {
      content: "";
      width: 30px;
      height: 2px;
      background-color: $black;
      bottom: 0px;
      animation: loadingLocation 2s infinite;
      display: block;
      position: absolute;
    }
  }

  .status-empty,
  .status-new {
    &:before {
      background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='130F0B' viewBox='0 0 24 24'%3E%3Cpath d='M12,2a8,8,0,0,0-8,8c0,5.4,7.05,11.5,7.35,11.76a1,1,0,0,0,1.3,0C13,21.5,20,15.4,20,10A8,8,0,0,0,12,2Zm0,17.65c-2.13-2-6-6.31-6-9.65a6,6,0,0,1,12,0C18,13.34,14.13,17.66,12,19.65ZM12,6a4,4,0,1,0,4,4A4,4,0,0,0,12,6Zm0,6a2,2,0,1,1,2-2A2,2,0,0,1,12,12Z'/%3E%3C/svg%3E")
        no-repeat;
      left: -3px;
      top: -1px;
    }
  }

  .status-geocoded {
    &:before {
      background: url("/static/images/leaflet/custom-marker.png") no-repeat;
      background-size: 13px;
    }
  }

  .status-unknown {
    input {
      border-bottom: 1px solid red !important;
      color: red;
    }

    &:before {
      background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='red' viewBox='0 0 24 24'%3E%3Cpath d='M11.29,15.29a1.58,1.58,0,0,0-.12.15.76.76,0,0,0-.09.18.64.64,0,0,0-.06.18,1.36,1.36,0,0,0,0,.2.84.84,0,0,0,.08.38.9.9,0,0,0,.54.54.94.94,0,0,0,.76,0,.9.9,0,0,0,.54-.54A1,1,0,0,0,13,16a1,1,0,0,0-.29-.71A1,1,0,0,0,11.29,15.29ZM12,2A10,10,0,1,0,22,12,10,10,0,0,0,12,2Zm0,18a8,8,0,1,1,8-8A8,8,0,0,1,12,20ZM12,7A3,3,0,0,0,9.4,8.5a1,1,0,1,0,1.73,1A1,1,0,0,1,12,9a1,1,0,0,1,0,2,1,1,0,0,0-1,1v1a1,1,0,0,0,2,0v-.18A3,3,0,0,0,12,7Z'/%3E%3C/svg%3E")
        no-repeat;
      background-position: left 0px bottom 3px;
    }
  }
}

@keyframes bounceMarker {
  0%,
  25%,
  50%,
  75%,
  100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-3px);
  }
  60% {
    transform: translateY(-1px);
  }
}

@keyframes loadingLocation {
  0%,
  100% {
    left: 0px;
  }
  50% {
    left: calc(100% - 30px);
  }
}
</style>
