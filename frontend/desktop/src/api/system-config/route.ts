import { defHttp } from '/@/utils/http/axios';
import {BasicSelectionResult} from "/@/api/model/baseModel";

enum Api {
  GetDataRouteSelection = '/route/get-selection',
}

export const apiGetDataRouteSelection = () => {
  return defHttp.get<BasicSelectionResult[]>(
    {
      url: Api.GetDataRouteSelection,
    }
  )
}
