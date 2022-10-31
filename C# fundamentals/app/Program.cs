// See https://aka.ms/new-console-template for more information
using System;
using System.Collections.Generic;
using Newtonsoft.Json;
using System.Drawing.Imaging;
using System.Drawing;
using System.Web.Http;
using System.Web;

// libraries to be used:
// RestSharp    - simple REST and HTTP API Client
// Json.NET     - Json.NET is a popular high-performance JSON framework for .NET

namespace Console
{
	class ApiHelper
	{
		static void Main(string[] args)
		{
			var client = new HttpClient();

			// read the image as a bitmap
			using (Bitmap image_bmp = new Bitmap(Image.FromFile("C:/AI_semester_6/imagesForICR/imagesforICR/findCharacters.png")))
			{
				// convert bitmap to byte array - using MemoryStream for not writing to hard disk - https://stackoverflow.com/questions/12645705/c-bitmap-to-byte-array
				using (var memoryStream = new MemoryStream())
				{

					image_bmp.Save(memoryStream, System.Drawing.Imaging.ImageFormat.Jpeg);
					var response = client.PostAsJsonAsync( "http://localhost:5000/api/v1.0/process_img",  
					// var response = client.PostAsJsonAsync( "http://172.31.48.20:5000/api/v1.0/process_img",
						new  {
							message = "",
							content = Convert.ToBase64String(memoryStream.ToArray()),   
							// converting bitmap to byte array -  https://stackoverflow.com/questions/12645705/c-bitmap-to-byte-array
							// sending request using PostAsJsonAsync - https://stackoverflow.com/questions/15205389/get-response-from-postasjsonasync
						}
					);
					System.Console.WriteLine(response.Result.ToString());
					System.Console.WriteLine(response.Result.RequestMessage);
				}                               
			}
		}
		
		public static byte[] ImageToByte(Image img)
		{
			using (var stream = new MemoryStream())
			{
				img.Save(stream, System.Drawing.Imaging.ImageFormat.Png);
				return stream.ToArray();
			}
		}
	}
}
// "C:/AI_semester_6/imagesForICR/imagesforICR/findCharacters.png"
