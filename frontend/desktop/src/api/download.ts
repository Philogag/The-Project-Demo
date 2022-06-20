import { defHttp } from '/@/utils/http/axios';
import { message, notification } from 'ant-design-vue';

export function blobShowDownload(data: Blob, filename?: string) {
  // @ts-ignore
  const url = window.URL || window.webkitURL || window.moxURL;
  const link = document.createElement('a');
  link.href = url.createObjectURL(data);
  link.setAttribute('download', filename ? filename : '');
  link.style.display = 'none';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  url.revokeObjectURL(link.href);
}

function blobToJson(data: Blob) {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.readAsText(data, 'utf-8');
    reader.onload = function () {
      try {
        resolve(JSON.parse(reader.result as string));
      } catch (error) {
        resolve(undefined);
      }
    };
  });
}

function getFileName(contentDisposition) {
  const filenameRegex = /filename\*=UTF-8''(.*)/;
  const matches = filenameRegex.exec(contentDisposition);
  if (matches != null && matches[1]) {
    return decodeURIComponent(matches[1]);
  } else {
    return undefined;
  }
}

export function downloadFile(file_url) {
  message.loading({duration: 0, content: '文件构建中 ...'})
  return defHttp
    .get<any>({ url: file_url, responseType: 'blob' }, { isReturnNativeResponse: true })
    .then(async (res) => {
      message.destroy();
      const blob = new Blob([res.data]);
      if (res.headers['content-type'] === 'application/json') {
        const data = await blobToJson(blob);
        if (data !== undefined) {
          notification.error({
            message: '下载失败',
            // @ts-ignore
            description: data?.message.join('\n'),
            duration: 4,
          });
        } else {
          // @ts-ignore
          message.error('下载错误：未知错误');
        }
      } else {
        // get file!
        const filename = getFileName(res.headers['content-disposition']);
        blobShowDownload(blob, filename);
      }
    });
}
