from functions import *

# Get the parent directory
parent_dir = os.path.dirname(current_directory)
def process_video(source:str=parent_dir+'\\data\\input\\input2.mp4',
				  save_video:bool=True,
				  show_video:bool=True,
				  save_image:bool=True,
				  out_path:str=parent_dir+'\\data\\output\\output.mp4'):
	# Initialize video writer
	fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' codec for .mp4 output
	out = cv2.VideoWriter(parent_dir + '\\data\\output\\output.mp4', fourcc, 20.0, frame_size)
	cap = cv2.VideoCapture(source)
	while(cap.isOpened()):
		ret, frame = cap.read()
		if ret == True:
			frame = cv2.resize(frame, frame_size)  # resizing image
			orifinal_frame = frame.copy()
			frame, results = object_detection(frame) 

			rider_list = []
			head_list = []
			number_list = []

			for result in results:
				x1,y1,x2,y2,cnf, clas = result
				if clas == 0:
					rider_list.append(result)
				elif clas == 1:
					head_list.append(result)
				elif clas == 2:
					number_list.append(result)

			for rdr in rider_list:
				time_stamp = str(time.time())
				x1r, y1r, x2r, y2r, cnfr, clasr = rdr
				for hd in head_list:
					x1h, y1h, x2h, y2h, cnfh, clash = hd
					if inside_box([x1r,y1r,x2r,y2r], [x1h,y1h,x2h,y2h]): # if this head inside this rider bbox
						try:
							head_img = orifinal_frame[y1h:y2h, x1h:x2h]
							helmet_present = img_classify(head_img)
						except:
							helmet_present[0] = None

						# detect helmet, if not wear helmet -> save image
						if  helmet_present[0] == True: # if helmet present
							frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0,255,0), 1)
							frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
						elif helmet_present[0] == None: # Poor prediction
							frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 255, 255), 1)
							frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
						elif helmet_present[0] == False: # if helmet absent 
							frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 0, 255), 1)
							frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
							try:
								cv2.imwrite(parent_dir+f'/data/output/riders_pictures/{time_stamp}.jpg', frame[y1r:y2r, x1r:x2r])
							except:
								print('could not save rider')

							for num in number_list:
								x1_num, y1_num, x2_num, y2_num, conf_num, clas_num = num
								if inside_box([x1r,y1r,x2r,y2r], [x1_num, y1_num, x2_num, y2_num]):
									try:
										num_img = orifinal_frame[y1_num:y2_num, x1_num:x2_num]
										cv2.imwrite(parent_dir+f'/data/output/number_plates/{time_stamp}_{conf_num}.jpg', num_img)
									except:
										print('could not save number plate')
										
			if save_video: # save video
				out.write(frame)
			if save_img: #save img
				cv2.imwrite('saved_frame.jpg', frame)
			if show_video: # show video
				frame = cv2.resize(frame, (900, 450))  # resizing to fit in screen
				cv2.imshow('Frame', frame)


			if cv2.waitKey(1) & 0xFF == ord('q'):
				break	
		else:
			break

	cap.release()
	cv2.destroyAllWindows()
	print('Execution completed')
	

# Configuration
source = current + '\\input\\input2.mp4'  # Specify the path to the MP4 video file
save_video = True  # Save processed video
show_video = True  # Display the video while processing
save_img = True  # Save individual frames as images	
process_video(source=source, save_video=save_video, save_image=save_img, show_video=show_video)