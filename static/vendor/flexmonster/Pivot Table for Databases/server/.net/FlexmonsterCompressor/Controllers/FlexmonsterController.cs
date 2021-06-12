using System.Data.Common;
using System.Data.SqlClient;
using System.IO;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Web.Http;

namespace FlexmonsterCompressor.Controllers
{
    public class FlexmonsterController : ApiController
    {
        [HttpGet]
        public HttpResponseMessage Get()
        {
            // connect to database
            string connectionString = "Data Source=localhost;Initial Catalog=AdventureWorks2012;Trusted_Connection=True;";
            SqlConnection sqlConnection = new SqlConnection(connectionString);
            sqlConnection.Open();

            // query for dataset
            string query = "SELECT * FROM Production.Product";
            DbCommand command = new SqlCommand(query, sqlConnection);
            DbDataReader dataReader = command.ExecuteReader();

            // get compressed stream
            Stream inputStream = Flexmonster.Compressor.Compressor.CompressDb(dataReader);

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
