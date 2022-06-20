<template>
  <PageWrapper>
    <div class="lg:flex">
      <div class="lg:w-3/10 w-full enter-y">
        <template v-for="item in navBlocks" :key="item.title">
          <QuickNav 
            class="enter-y"
            :title="item.title"
            :items="item.items"
            :loading="loading"
          />
        </template>
      </div>
    </div>
  </PageWrapper>
</template>
<script lang="ts">
  import { defineComponent, onMounted, ref } from 'vue';
  import { PageWrapper } from '/@/components/Page';
  import QuickNav from '../components/QuickNav.vue';
  import { apiGetPinnedSportMeeting } from '/@/api/data-view/sport-meeting';

  export default defineComponent({
    name: 'TeamLeaderDashboard',
    components:{
      PageWrapper,
      QuickNav,
    },
    setup (porps) {
      const loading = ref(true);
      const sportMeetingList = ref<any[]>([]);
      const navBlocks = ref<any[]>([]);

      onMounted(async () => {
        sportMeetingList.value = await apiGetPinnedSportMeeting();
        navBlocks.value = sportMeetingList.value
          .filter((item) => item?.teamId)
          .map((item) => ({
            title: item.name,
            items: [
              {
                title: '信息总览',
                icon: 'ion:grid-outline',
                color: '#bf0c2c',
                route: {
                  path: `/sport-meeting/${item.id}/mobile/guest`,
                  query: { page: 'ScoreRank', }
                },
              },
              {
                title: '队伍信息',
                icon: 'ion:layers-outline',
                color: '#1fdaca',
                route: {
                  path: `/sport-meeting/${item.id}/mobile/team/${item.teamId}`,
                  query: { page: 'TeamScoreViewer', }
                },
              },
              // {
              //   title: '成绩录入',
              //   icon: 'ion:layers-outline',
              //   color: '#e18525',
              //   route: {
              //     path: `/sport-meeting/${item.id}/mobile/team/${item.teamId}`,
              //     query: { page: 'CompetitionList', }
              //   },
              // },
            ]
          }))
        loading.value = false;
      })

      return {
        loading,
        sportMeetingList,
        navBlocks,
      }
    }
  })
</script>
