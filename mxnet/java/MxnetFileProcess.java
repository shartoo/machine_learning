package bot;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.security.KeyStore.Entry;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Random;
import java.util.Set;

/**
 * 处理mxnet结果的相关文件操作
 * @author hdfs
 *
 */
public class MxnetFileProcess {

	   /**
     * 保存处理的最终结果
     * @param file		保存结果路径
     * @param content	需要保存的内容
     */
    public void saveResult(String file,String content){
    	FileOutputStream out = null; 
    	 try {     
             out = new FileOutputStream(new File(file));     
             long begin = System.currentTimeMillis();         
             out.write(content.getBytes());
             out.close();     
    	 }catch(Exception e){
    		 e.printStackTrace();
    	 }
    	 System.out.println("Write result finished!.....");
    }
    
    /**
     * mxnet预测结果可能是 每个标签各有多少置信度，此方法可将置信度直接转换为标签
     * @param mxnetDirectResult   mxnet预测的文本格式文件
     * @param standardOut			  提交比赛结果的格式文件
     */
	public void toStandardPredictResult(String mxnetDirectResult,String standardOut){
		File file = new File(mxnetDirectResult);
		
		StringBuilder standardResultStr = new StringBuilder();		
		try{
			BufferedReader reader = new BufferedReader(new FileReader(file));
			String tmpStr = "";
			while((tmpStr=reader.readLine())!=null){
				String[] strings = tmpStr.split("\t|,");
				String[] filenames = strings[0].split("/");
				String justFileName =filenames[Math.max(0,filenames.length-1)].replace(".jpg", "");
				standardResultStr.append(justFileName).append(",");
				String maxLabel="";
				double maxProp =0.0;
				for(int i=1;i<strings.length;i=i+2)
				{
					String tmpLabel = strings[i];
					try{
					double tmpProp =Double.parseDouble(strings[i+1]);
					if (tmpProp>maxProp)
					{
						maxProp =tmpProp;
						maxLabel =tmpLabel;
//						if (maxProp<0.5)
//							maxLabel ="0";
					}	
					}catch(Exception e){
						e.printStackTrace();
					}
				}
				standardResultStr.append(maxLabel);
				standardResultStr.append("\r\n");
			}
			reader.close();
		}catch (IOException e){
			e.printStackTrace();
		}
		String saveFilName = mxnetDirectResult.replace(file.getName(), "standard_"+file.getName().split("\\.")[0]+".csv");
		if(null==standardOut)
			standardOut =saveFilName;
		saveResult(standardOut,standardResultStr.toString());
	}
	
	/**
	 * 从文件中读取图片列表
	 * @param file      包含了图片名称的列表
	 * @param index  图片名称所在列
	 * @param sepator  文件中列之间分隔符
	 * @return
	 */
	public ArrayList<String> readFileList(String file,int index,String sepator){
		ArrayList<String> list=new ArrayList<String>();
		File fRead=new File(file);
		BufferedReader bufferedReader =null;	
		try{
			bufferedReader = new BufferedReader(new FileReader(fRead));
			String tmpStr ="";
			while(null!=(tmpStr=bufferedReader.readLine())){
				  String name = tmpStr.split(sepator)[index];
				  list.add(name.trim());
			}
		}catch(IOException e){
			e.printStackTrace();
		}
		return list;
	}
	/**
	 * 根据概率生成标签分布
	 * @param imgNameList		需要处理的图片标签列表
	 * @param targetFile			      生成的图片与标签内容要保存的文件名		
	 * @param labelAndProp		标签和对应出现的概率。注意概率之和要为1  {"1":0.76,"0":0.24}
	 */
	public void generatePropLabel(ArrayList<String> imgNameList,String targetFile,HashMap<String, Double> labelAndProp){
		Random random = new Random();
		Set<Map.Entry<String,Double>> entry =labelAndProp.entrySet();
		Iterator<Map.Entry<String, Double>> iterator = entry.iterator();
		ArrayList<String> labels = new ArrayList<String>();
		ArrayList<Double> props = new ArrayList<Double>();
		double sumProp=0.0;
		while(iterator.hasNext()){
			Map.Entry<String,Double> entry2=iterator.next();
			labels.add(entry2.getKey());
			//将概率变为累计概率
			sumProp = sumProp+entry2.getValue();
			props.add(sumProp);
		}
		
		StringBuilder stringBuilder= new StringBuilder();
		int propNum = props.size()-1;
		for(String img:imgNameList)
		{
			double p = random.nextDouble();
			String realLabel ="";
			//概率列表是从前往后累加的，所以找到当前随机概率的区间是从后往前
			for(int i=propNum;i>=0;i--)
			{
				double propOfList = props.get(i);
				if(p>propOfList)
					   break;    //已经找到了累计概率所在位置
				realLabel = labels.get(i);
			}
			stringBuilder.append((img+","+realLabel).replaceAll("\\s+", "")).append("\r\n");
		}
		//保存结果到文件
		saveResult(targetFile,stringBuilder.toString());
	}
}
