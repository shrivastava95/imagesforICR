using System.Text;
using Newtonsoft.Json;

var person = new Person("John Doe", "gardener");

var json = JsonConvert.SerializeObject(person);
var data = new StringContent(json, Encoding.UTF8, "application/json");

var url = "http://localhost:5000/api/v1.0/process_img";

using var client = new HttpClient();

var response = await client.PostAsync(url, data);

var result = await response.Content.ReadAsStringAsync();
Console.WriteLine(result);

record Person(string Name, string Occupation);

