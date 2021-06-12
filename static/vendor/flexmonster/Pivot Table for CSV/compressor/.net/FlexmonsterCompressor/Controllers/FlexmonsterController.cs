using System.IO;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Web.Hosting;
using System.Web.Http;

namespace FlexmonsterCompressor.Controllers
{
    public class FlexmonsterController : ApiController
    {
        [HttpGet]
        public HttpResponseMessage Get()
        {
            // get compressed stream
            Stream inputStream = Flexmonster.Compressor.Compressor.CompressFile(HostingEnvironment.MapPath("~/App_Data/data.csv"));

            // return streaming response
            HttpResponseMessage response = Request.CreateResponse();
            response.Content = new PushStreamContent((Stream outputStream, HttpContent content, TransportContext context) =>
            {
                int count = 0;
                byte[] buffer = new byte[10240];
                while ((count = inputStream.Read(buffer, 0, buffer.Length)) > 0)
                {
                    outputStream.Write(buffer, 0, count);
                    outputStream.Flush();
                }
                outputStream.Close();
            }, new MediaTypeHeaderValue("text/plain"));
            return response;
        }
    }
}
